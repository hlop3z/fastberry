"""
    Fastberry Main (Core-Methods)
"""

from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission

from . import config

# from .config import Settings
from .config import Settings as Fastberry
from .config.extras.gql import GQL

# from .graphql import BaseType
from .schema import Schema
from .types import Model, SQLFilters

Text = Model.text
JSON = Model.json
