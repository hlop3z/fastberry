import importlib
import pkgutil

get_fields = lambda model: [i for i in dir(model) if not i.startswith("__")]


def iter_namespace(ns_pkg):
    """https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/"""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def import_modules(all_apps):
    """https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/"""
    installed_apps = {}
    for app in all_apps:
        try:
            module = importlib.import_module(app)
        except:
            module = None
        if module:
            discovered_plugins = {
                name: importlib.import_module(name)
                for finder, name, ispkg in iter_namespace(module)
            }
            installed_apps.update(discovered_plugins)
    return installed_apps
