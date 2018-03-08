
import os

CURRENT_PACKAGE_FILE   = os.path.dirname( os.path.realpath( __file__ ) )
PACKAGE_ROOT_DIRECTORY = CURRENT_PACKAGE_FILE.replace( ".py", "" )
CURRENT_PACKAGE_NAME   = os.path.basename( PACKAGE_ROOT_DIRECTORY )

from debug_tools import getLogger
log = getLogger(1, CURRENT_PACKAGE_NAME)


from .plugin.core.main import startup, shutdown, LspStartClientCommand, LspRestartClientCommand

# TODO: narrow down imports
from .plugin.core.panels import *
from .plugin.core.documents import *
from .plugin.core.edit import *
from .plugin.completion import *
from .plugin.diagnostics import *
from .plugin.configuration import *
from .plugin.formatting import *
from .plugin.highlights import *
from .plugin.definition import *
from .plugin.hover import *
from .plugin.references import *
from .plugin.signature_help import *
from .plugin.code_actions import *
from .plugin.symbols import *
from .plugin.rename import *


def plugin_loaded():
    startup()


def plugin_unloaded():
    shutdown()

