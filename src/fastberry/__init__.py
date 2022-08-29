"""
    Fastberry Main (Core-Methods)
"""
import dataclasses as dc
import datetime as DATETIME
import decimal as DECIMAL
import typing

import dbcontroller as dbc
import strawberry
from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission

from .config import Settings as Fastberry
from .config.extras.gql import GQL
from .schema import Schema
from .utils.coro import coro
from .utils.to_camel_case import to_camel_case

# Database
Database = dbc.Database
Model = dbc.Model

# Custom Field Types
ID = dbc.ID
JSON = dbc.JSON
Text = dbc.Text

# Easy Access
text = dbc.Text
json = dbc.json
date = DATETIME.date
datetime = DATETIME.datetime
time = DATETIME.time
decimal = DECIMAL.Decimal
ref = typing.Optional

# Data-Class: < Maker >
input = dbc.input
search = dbc.search
crud = dbc.crud
form = dbc.form

# Data-Class: < Fields >
field = dbc.field
filters = dbc.filters

# Strawberry.TYPE
type = strawberry.type


def default(method):
    """Default Value For Type(s)"""
    default_value = None
    if callable(method):
        default_value = dc.field(default_factory=method)
    else:
        default_value = dc.field(default=method)
    return default_value


class Date:
    """Date Functions"""

    @staticmethod
    def datetime():
        return DATETIME.datetime.now()

    @staticmethod
    def date():
        return DATETIME.date.today()

    @staticmethod
    def time():
        return DATETIME.datetime.now().time()
