"""
    Fastberry Main (Core-Methods)
"""
from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission

from pathlib import Path

try:
    import spoc
except:
    if not Path("./config").exists():
        Path("./config").mkdir()

    file_settings = "./config/settings.py"
    if not Path(file_settings).exists():
        with open(file_settings, "w") as f:
            f.write(
                """
# -*- coding: utf-8 -*-
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
# INSTALLED_APPS = []

# SQL_URL = "sqlite:///example.db"
# MONGO_URL = "mongodb://localhost:27017/test_database"            
""".strip()
            )

    file_settings = "./config/spoc.toml"
    if not Path(file_settings).exists():
        with open(file_settings, "w") as f:
            f.write(
                """
[spoc]
mode = "custom"
custom_mode = "development"
docs = "config/docs.md"
generates = "graphql"

[spoc.api]
graphql_path = "/graphql"
max_depth = 4
items_per_page = 50
allowed_hosts = ["http://localhost", "http://localhost:8080"]

[spoc.apps]
production = []
development = []
staging = []

[spoc.extra]
middleware = []
extensions = []
permissions = []
on_startup = ["fastberry.extras.redirect_root"] # "fastberry.extras.graphql_info"
on_shutdown = []
""".strip()
            )

    file_settings = "./config/docs.md"
    if not Path(file_settings).exists():
        with open(file_settings, "w") as f:
            f.write(
                """
# Welcome

> This is a simple **API** Skeleton

---

## Links

> Go To [GraphQL](/graphql)

---

## Mode (Options)

- `development`

- `staging`

- `production`

---

## Settings Layout

```text
root/                           --> <Directory> - Project's Root.
|
|--  config/                    --> <Directory> - Configurations.
|    |
|    |-- .env/                  --> <Directory> - Environments.
|    |   |
|    |   |-- development.toml   --> <File> - Development | Settings.
|    |   |-- production.toml    --> <File> - Production | Settings.
|    |   `-- staging.toml       --> <File> - Staging | Settings.
|    |
|    |-- docs.md                --> <File> - This Documentation is in HERE.
|    |-- settings.py            --> <File> - Python | Settings.
|    `-- spoc.toml              --> <File> - TOML | Settings.
|
|-- pyproject.toml              --> <File> - Project | Settings.
|
`-- etc...
```
""".strip()
            )

    import spoc

# FrameWork
from .components import APIRouter as Router
from .components import cli
from .components import graphql as gql
from .framework import Fastberry as App

# GraphQL Tools
from .graphql import edges, error, errors, mutation, page, query

# GraphQL Premade User-Inputs
from .tools import Item as item
from .tools import Pagination as pagination

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
