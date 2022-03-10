# Core
from .database import mongo, sql
from .imports import settings

# Loop Over Apps
from .models import model_to_dict
from .plugins import import_modules

"""
########  ########   #######        ## ########  ######  ######## 
##     ## ##     ## ##     ##       ## ##       ##    ##    ##    
##     ## ##     ## ##     ##       ## ##       ##          ##    
########  ########  ##     ##       ## ######   ##          ##    
##        ##   ##   ##     ## ##    ## ##       ##          ##    
##        ##    ##  ##     ## ##    ## ##       ##    ##    ##    
##        ##     ##  #######   ######  ########  ######     ##    
"""

ALL_PLUGINS = {}


def init_models():
    global ALL_PLUGINS
    all_models = None
    if settings and hasattr(settings, "INSTALLED_APPS"):
        installed_apps = import_modules(settings.INSTALLED_APPS)
        all_models = model_to_dict(installed_apps)
    if all_models:
        ALL_PLUGINS.update(all_models)
    return all_models


class Model:
    __plugins = ALL_PLUGINS

    @classmethod
    def get(cls, model):
        return cls.__plugins.get(model)

    @classmethod
    def all(cls):
        return cls.__plugins

    @classmethod
    def keys(cls):
        return list(cls.__plugins.keys())


# print(all_models.keys())
# print(installed_apps.keys())
