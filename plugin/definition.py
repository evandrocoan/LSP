import sublime

from debug_tools import getLogger

from .core.registry import client_for_view, LspTextCommand
from .core.protocol import Request, Point
from .core.documents import get_document_position, get_position, is_at_word
from .core.url import uri_to_filename

from Default.history_list import get_jump_history_for_view

try:
    from typing import List, Dict, Optional, Any
    assert List and Dict and Optional and Any
except ImportError:
    pass

log = getLogger(1, __name__)

class LspSymbolDefinitionCommand(LspTextCommand):
    def __init__(self, view):
        super().__init__(view)

    def is_enabled(self, event=None):
        if self.has_client_with_capability('definitionProvider'):
            return is_at_word(self.view, event)
        return False

    def run(self, edit, event=None) -> None:
        client = client_for_view(self.view)
        if client:
            pos = get_position(self.view, event)
            document_position = get_document_position(self.view, pos)
            if document_position:
                request = Request.definition(document_position)
                client.send_request(
                    request, lambda response: self.handle_response(response, pos))

    def handle_response(self, response: 'Optional[Any]', position) -> None:
        window = sublime.active_window()
        if response:
            # save to jump back history
            get_jump_history_for_view(self.view).push_selection(self.view)

            # https://github.com/SublimeTextIssues/Core/issues/1482
            group, view_index = window.get_view_index(self.view)
            window.set_view_index(self.view, group, 0)

            location = response if isinstance(response, dict) else response[0]
            file_path = uri_to_filename(location.get("uri"))
            start = Point.from_lsp(location['range']['start'])
            file_location = "{}:{}:{}".format(file_path, start.row + 1, start.col + 1)
            log(2, "opening location %s <%s>", location, file_location)
            window.open_file(file_location, sublime.ENCODED_POSITION)
            window.set_view_index(self.view, group, view_index)
            # TODO: can add region here.
        else:
            window.run_command("goto_definition")

    def want_event(self):
        return True
