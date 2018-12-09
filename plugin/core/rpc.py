import json
import socket
import time
from .transports import TCPTransport, StdioTransport, Transport
from .process import attach_logger
try:
    import subprocess
    from typing import Any, List, Dict, Tuple, Callable, Optional, Union
    # from mypy_extensions import TypedDict
    assert Any and List and Dict and Tuple and Callable and Optional and Union and subprocess
except ImportError:
    pass

from debug_tools import getLogger

from .settings import PLUGIN_NAME
from .protocol import Request, Notification, Response
from .types import Settings


log = getLogger(1, __name__)

TCP_CONNECT_TIMEOUT = 5

# RequestDict = TypedDict('RequestDict', {'id': 'Union[str,int]', 'method': str, 'params': 'Optional[Any]'})


def format_request(payload: 'Dict[str, Any]') -> str:
    """Converts the request into json and adds the Content-Length header"""
    content = json.dumps(payload, sort_keys=False)
    content_length = len(content)
    result = "Content-Length: {}\r\n\r\n{}".format(content_length, content)
    return result


def attach_tcp_client(tcp_port: int, process: 'subprocess.Popen', settings: Settings) -> 'Optional[Client]':
    if settings.log_stderr:
        attach_logger(process, process.stdout)

    host = "localhost"
    start_time = time.time()
    log(2, 'connecting to %s:%s', host, tcp_port)

    while time.time() - start_time < TCP_CONNECT_TIMEOUT:
        try:
            sock = socket.create_connection((host, tcp_port))
            transport = TCPTransport(sock)

            client = Client(transport, settings)
            client.set_transport_failure_handler(lambda: try_terminate_process(process))
            return client
        except ConnectionRefusedError as e:
            pass

    process.kill()
    raise Exception("Timeout connecting to socket")


def attach_stdio_client(process: 'subprocess.Popen', settings: Settings) -> 'Client':
    transport = StdioTransport(process)

    # TODO: process owner can take care of this outside client?
    if settings.log_stderr:
        attach_logger(process, process.stderr)
    client = Client(transport, settings)
    client.set_transport_failure_handler(lambda: try_terminate_process(process))
    return client


def try_terminate_process(process: 'subprocess.Popen') -> None:
    try:
        process.terminate()
    except ProcessLookupError:
        pass  # process can be terminated already


class Client(object):
    def __init__(self, transport: Transport, settings) -> None:
        self.transport = transport
        self.transport.start(self.receive_payload, self.on_transport_closed)
        self.request_id = 0
        self._response_handlers = {}  # type: Dict[int, Tuple[Optional[Callable], Optional[Callable]]]
        self._request_handlers = {}  # type: Dict[str, Callable]
        self._notification_handlers = {}  # type: Dict[str, Callable]
        self.exiting = False
        self._crash_handler = None  # type: Optional[Callable]
        self._transport_fail_handler = None  # type: Optional[Callable]
        self._error_display_handler = lambda msg: log(1, msg)
        self.settings = settings

    def send_request(self, request: Request, handler: 'Callable[[Optional[Any]], None]',
                     error_handler: 'Optional[Callable]' = None) -> None:
        self.request_id += 1
        log(2, ' --> %s', request.method)
        self._response_handlers[self.request_id] = (handler, error_handler)
        self.send_payload(request.to_payload(self.request_id))

    def send_notification(self, notification: Notification) -> None:
        log(2, ' --> %s', notification.method)
        self.send_payload(notification.to_payload())

    def send_response(self, response: Response) -> None:
        self.send_payload(response.to_payload())

    def exit(self) -> None:
        self.exiting = True
        self.send_notification(Notification.exit())

    def set_crash_handler(self, handler: 'Callable') -> None:
        self._crash_handler = handler

    def set_error_display_handler(self, handler: 'Callable') -> None:
        self._error_display_handler = handler

    def set_transport_failure_handler(self, handler: 'Callable') -> None:
        self._transport_fail_handler = handler

    def handle_transport_failure(self) -> None:
        if self._transport_fail_handler is not None:
            self._transport_fail_handler()
        if self._crash_handler is not None:
            self._crash_handler()

    def send_payload(self, payload: 'Dict[str, Any]') -> None:
        message = format_request(payload)
        self.transport.send(message)

    def receive_payload(self, message: str) -> None:
        payload = None
        try:
            payload = json.loads(message)
            # limit = min(len(message), 200)
            # log(2, "got json: %s ...", message[0:limit])
        except IOError as err:
            log.exception("got a non-JSON payload: %s", message)
            return

        try:
            if "method" in payload:
                if "id" in payload:
                    self.request_handler(payload)
                else:
                    self.notification_handler(payload)
            elif "id" in payload:
                self.response_handler(payload)
            else:
                log(2, "Unknown payload type: %s", payload)
        except Exception as err:
            log.exception("Error handling server payload")

    def on_transport_closed(self) -> None:
        self._error_display_handler("Communication to server closed, exiting")
        # Differentiate between normal exit and server crash?
        if not self.exiting:
            self.handle_transport_failure()

    def response_handler(self, response: 'Dict[str, Any]') -> None:
        request_id = int(response["id"])
        if self.settings.log_payloads:
            log(2, '     %s', response.get("result", None))
        handler, error_handler = self._response_handlers.pop(request_id, (None, None))
        if "result" in response and "error" not in response:
            if handler:
                handler(response["result"])
            else:
                log(2, "No handler found for id %s", request_id)
        elif "result" not in response and "error" in response:
            error = response["error"]
            if error_handler:
                error_handler(error)
            else:
                self._error_display_handler(error.get("message"))
        else:
            log(2, 'invalid response payload %s', response)

    def on_request(self, request_method: str, handler: 'Callable') -> None:
        self._request_handlers[request_method] = handler

    def on_notification(self, notification_method: str, handler: 'Callable') -> None:
        self._notification_handlers[notification_method] = handler

    def request_handler(self, request: 'Dict[str, Any]') -> None:
        request_id = request.get("id")
        params = request.get("params", dict())
        method = request.get("method", '')
        log(2, '<--  %s', method)
        if self.settings.log_payloads and params:
            log(2, '     %s', params)
        if method in self._request_handlers:
            try:
                self._request_handlers[method](params, request_id)
            except Exception as err:
                log.exception("Error handling request %s", method)
        else:
            log(2, "Unhandled request %s", method)

    def notification_handler(self, notification: 'Dict[str, Any]') -> None:
        method = notification["method"]
        params = notification.get("params")
        if method == "window/logMessage":
            log(2, '<--  ' + method)
            log.clean(2, "%s server: %s", PLUGIN_NAME, params.get("message", "???") if params else "???")
            return

        log(2, '<--  ' + method)
        if self.settings.log_payloads and params:
            log(2, '     ' + str(params))
        if method in self._notification_handlers:
            try:
                self._notification_handlers[method](params)
            except Exception as err:
                log.exception("Error handling notification %s", method)
        else:
            log(2, "Unhandled notification: %s", method)
