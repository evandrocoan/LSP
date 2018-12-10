import os
try:
    from typing import List, Optional, Any
    assert List and Optional and Any
except ImportError:
    pass

from debug_tools import getLogger
log = getLogger(1, __name__)
# from .types import WindowLike


def get_project_path(window: 'Any') -> 'Optional[str]':
    """
    Returns the first project folder or the parent folder of the active view
    """
    if len(window.folders()):
        folder_paths = window.folders()
        return folder_paths[0]
    else:
        view = window.active_view()
        if view:
            filename = view.file_name()
            if filename:
                project_path = os.path.dirname(filename)
                log(2, "Couldn't determine project directory since no folders are open!",
                      "Using", project_path, "as a fallback.")
                return project_path
            else:
                log(2, "Couldn't determine project directory since no folders are open",
                      "and the current file isn't saved on the disk.")
                return None
        else:
            log(2, "No view is active in current window")
            return None  # https://github.com/tomv564/LSP/issues/219


def get_common_parent(paths: 'List[str]') -> str:
    """
    Get the common parent directory of multiple paths.

    Python 3.5+ includes os.path.commonpath which does this, however Sublime
    currently embeds Python 3.3.
    """
    return os.path.commonprefix([path + '/' for path in paths]).rstrip('/')


def is_in_workspace(window: 'Any', file_path: str) -> bool:
    workspace_path = get_project_path(window)
    if workspace_path is None:
        return False

    common_dir = get_common_parent([workspace_path, file_path])
    return workspace_path == common_dir


def enable_in_project(window, config_name: str) -> None:
    project_data = window.project_data()
    if isinstance(project_data, dict):
        project_settings = project_data.setdefault('settings', dict())
        project_lsp_settings = project_settings.setdefault('LSP', dict())
        project_client_settings = project_lsp_settings.setdefault(config_name, dict())
        project_client_settings['enabled'] = True
        window.set_project_data(project_data)
    else:
        log(2, 'non-dict returned in project_settings: %s', project_data)


def disable_in_project(window, config_name: str) -> None:
    project_data = window.project_data()
    if isinstance(project_data, dict):
        project_settings = project_data.setdefault('settings', dict())
        project_lsp_settings = project_settings.setdefault('LSP', dict())
        project_client_settings = project_lsp_settings.setdefault(config_name, dict())
        project_client_settings['enabled'] = False
        window.set_project_data(project_data)
    else:
        log(2, 'non-dict returned in project_settings: %s', project_data)


def get_project_config(window: 'Any') -> dict:
    project_data = window.project_data() or dict()
    if isinstance(project_data, dict):
        project_settings = project_data.setdefault('settings', dict())
        project_lsp_settings = project_settings.setdefault('LSP', dict())
        return project_lsp_settings
    else:
        log(2, 'non-dict returned in project_settings: %s', project_data)
        return dict()
