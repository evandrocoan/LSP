import sublime
import os
import sys
from .sessions import create_session, Session

# typing only
from .rpc import Client
from .settings import ClientConfig, settings
assert Client and ClientConfig


try:
    from typing import Any, List, Dict, Tuple, Callable, Optional, Set
    assert Any and List and Dict and Tuple and Callable and Optional and Set
    assert Session
except ImportError:
    pass


def get_window_env(window: sublime.Window, config: ClientConfig) -> 'Tuple[List[str], Dict[str, str]]':

    # Create a dictionary of Sublime Text variables
    variables = window.extract_variables()
    variables["sublime_path"] = os.path.dirname(sublime.executable_path())
    variables["sublime_libs"] = os.pathsep.join(sys.path)

    # Expand language server command line environment variables
    expanded_args = list(
        sublime.expand_variables(os.path.expanduser(arg), variables)
        for arg in config.binary_args
    )

    # Override OS environment variables
    env = os.environ.copy()
    for var, value in config.env.items():
        # Merge vars, e.g. PATH=$PATH;mypath (Windows), PATH=$PATH:mypath (Linux/OSX)
        # For ease of editing, allow lists for each environment variable
        if isinstance(value, list):
            value = os.pathsep.join(value)
        # Expand both ST and OS environment variables
        env[var] = os.path.expandvars(sublime.expand_variables(value, variables))

    return expanded_args, env


def start_window_config(window: sublime.Window, project_path: str, config: ClientConfig,
                        on_created: 'Callable', on_ended: 'Callable[[str], None]') -> 'Optional[Session]':
    args, env = get_window_env(window, config)
    config.binary_args = args
    return create_session(config, project_path, env, settings,
                          on_created=on_created,
                          on_ended=lambda config_name: on_session_ended(window, config.name, on_ended))


def on_session_ended(window: sublime.Window, config_name: str, on_ended_handler: 'Callable[[str], None]') -> None:
    on_ended_handler(config_name)
