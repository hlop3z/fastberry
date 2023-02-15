"""
    Fastberry Main (Core-Methods)
"""
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission

from .scripts import templates_code

try:
    import spoc
except:
    if not Path("./config").exists():
        Path("./config").mkdir()

    file_settings = "./config/settings.py"
    if not Path(file_settings).exists():
        with open(file_settings, "w", encoding="utf-8") as f:
            f.write(templates_code.SETTINGS)

    file_settings = "./config/spoc.toml"
    if not Path(file_settings).exists():
        with open(file_settings, "w", encoding="utf-8") as f:
            f.write(templates_code.SPOC)

    file_settings = "./config/docs.md"
    if not Path(file_settings).exists():
        with open(file_settings, "w", encoding="utf-8") as f:
            f.write(templates_code.DOCS)

    import spoc

# FrameWork
from .components import APIRouter as Router
from .components import cli
from .components import graphql as gql
from .framework import Fastberry as App

# GraphQL Tools
from .graphql import deleted, edges, editor, error, errors, mutation, page, query

# GraphQL Premade User-Inputs
from .tools import Item as item
from .tools import Pagination as pagination
from .tools import coro, doc

# Framework Wrappers
base_dir = spoc.base_dir
config = spoc.config
mode = spoc.mode
project = spoc.project
settings = spoc.settings

# Tools
component = spoc.component

try:
    import dbcontroller as dbc
    from dbcontroller.forms import ISNULL

    if hasattr(settings, "DATABASES"):
        config_sql = settings.DATABASES.get("sql")
        config_mongo = settings.DATABASES.get("mongo")
        default_sql = config_sql.get("default")
        default_mongo = config_mongo.get("default")
        if default_sql:
            sql = dbc.Controller(sql=default_sql)
        if default_mongo:
            mongo = dbc.Controller(mongo=default_mongo)

    # Types
    type = dbc.type

    # Forms
    input = dbc.form.graphql
    value = dbc.form.field

    # Value Tool
    filters = dbc.form.filters

    # Types Tool (DBController)
    field = dbc.field
    manager = dbc.manager

    # Scalars
    ID = dbc.ID
    date = dbc.date
    datetime = dbc.datetime
    time = dbc.time
    decimal = dbc.decimal
    text = dbc.text
    time = dbc.time
    json = dbc.json

    # Tester
    Date = dbc.Date

except ImportError:
    import strawberry

    # Types
    type = strawberry.type
    input = strawberry.input
