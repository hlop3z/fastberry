"""
    Default Databases
"""
import dataclasses as dc
import typing

import dbcontroller as dbc

from ...utils.objects import get_attr


@dc.dataclass(frozen=True)
class Database:
    """API (Default: Database) Manager"""

    sql: typing.Any = None
    mongo: typing.Any = None


@dc.dataclass(frozen=True)
class Model:
    """API (Default: Model) Manager"""

    sql: typing.Any = None
    mongo: typing.Any = None


def get_project_databases_settings(project):
    """Get Core Settings"""
    setup = {}
    if project:
        project_settings = get_attr(project, "settings")
        config_databases = get_attr(project_settings, "DATABASES")
        # Controller
        controller = dbc.Controller({}, fastberry=True)
        if config_databases:
            controller = dbc.Controller(config_databases, fastberry=True)
        setup["databases"] = controller
    return setup


def default_databases(self, API_TYPES):
    setup_models = {
        "sql": [],
        "mongo": [],
    }
    for model_config in API_TYPES.values():
        model_info = model_config.__meta__
        if model_info.database_name == "default" and model_info.is_super_class:
            if model_info.sql:
                setup_models["sql"].append(model_config)
            elif model_info.mongo:
                setup_models["mongo"].append(model_config)
    # ADMINS
    admin_sql = self.database.sql.admin(setup_models["sql"])
    admin_mongo = self.database.mongo.admin(setup_models["mongo"])

    return Model(
        sql=admin_sql,
        mongo=admin_mongo,
    )
