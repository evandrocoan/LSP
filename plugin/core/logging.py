import sys
import traceback
from .settings import settings, PLUGIN_NAME

def debug(*args):
    """Print args to the console if the "debug" setting is True."""
    if settings.log_debug:
        printf(*args)


def exception_log(message, ex):
    print(message)
    ex_traceback = ex.__traceback__
    print(''.join(traceback.format_exception(ex.__class__, ex, ex_traceback)))


def server_log(binary, *args):
    printf(*args, prefix=binary)


def printf(*args, prefix=PLUGIN_NAME):
    """Print args to the console, prefixed by the plugin name."""
    try:
        print(prefix + ":", *args)

    except Exception as error:
        sys.stderr.write("\n"*10)
        print(str(prefix))
        print(":")
        print(str(args))

        with open("D:/User/Downloads/LSP_issues_249.txt", "a", newline='\n') as text_file:
            text_file.write(str(prefix))
            text_file.write(":")
            text_file.write("\n")
            text_file.write(str(args))
            text_file.write(", Exception: ")
            text_file.write("\n")
            text_file.write(str(error))
            text_file.write("\n")

