"""Get App(s) Models - Inspire by Django

methods:
    process_models: Collect App Models.
"""

from dbcontroller.manager.mongo import MongoCrud
from dbcontroller.manager.sql import ManagerCrud

from ...utils.objects import get_fields

is_sql = lambda model: isinstance(model, ManagerCrud)
is_mongo = lambda model: isinstance(model, MongoCrud)


def process_models(app_name, app_module):
    """Collect App Models"""
    all_models = {}
    mod_name = app_name.replace(".models", "")
    for item in get_fields(app_module):
        model = getattr(app_module, item)
        is_model = False
        if is_mongo(model):
            model.engine = "mongo"
            is_model = True
        elif is_sql(model):
            model.engine = "sql"
            is_model = True
        if is_model:
            uri_name = f"{mod_name}.{item.lower()}"
            all_models[uri_name] = model
    return all_models
