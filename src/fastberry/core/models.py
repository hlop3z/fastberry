from dbcontroller.manager.mongo import MongoCrud
from dbcontroller.manager.sql import ManagerCrud

from .plugins import get_fields

get_models = lambda installed_apps: [
    app for app in installed_apps.keys() if app.endswith(".models")
]
get_api = lambda installed_apps: [
    app for app in installed_apps.keys() if app.endswith(".api")
]


is_sql = lambda model: isinstance(model, ManagerCrud)
is_mongo = lambda model: isinstance(model, MongoCrud)


def model_to_dict(installed_apps):
    all_models = dict()
    for model_module in get_models(installed_apps):
        module = installed_apps.get(model_module)
        fields = get_fields(module)
        for field in fields:
            model = getattr(module, field)
            if is_sql(model):
                manager = model
                all_models[field.lower()] = manager
            elif is_mongo(model):
                all_models[field.lower()] = model
    return all_models
