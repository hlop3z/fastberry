"""
    Auto-Importer
"""

import importlib
import pkgutil

from ..utils.objects import get_attr


def iter_namespace(ns_pkg):
    """https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/"""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def import_module(single_app: str):
    """Import Single-Module"""
    try:
        module = importlib.import_module(single_app)
    except:
        module = None
    return module


def import_modules(all_apps: list):
    """https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/"""
    installed_apps = {}
    for app in all_apps:
        module = import_module(app)
        if module:
            discovered_plugins = {
                name: importlib.import_module(name)
                for finder, name, ispkg in iter_namespace(module)
            }
            installed_apps.update(discovered_plugins)
    return installed_apps


def search_method(dotted_path: str):
    """Search for Method in <Module>"""
    parts = dotted_path.split(".")
    root = import_module(parts[0])
    module = root
    for part in parts[1:]:
        module = get_attr(module, part)
    return module
