"""
    Fastberry Main (Core-Methods)
"""

import strawberry
from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission

from . import config

# from .config import Settings
from .config import Settings as Fastberry
from .config.extras.gql import GQL

# from .graphql import BaseType
from .schema import Schema
from .types import Model
from .utils.coro import coro
from .utils.to_camel_case import to_camel_case

# Custom Field Types
Text = Model.text
JSON = Model.json
ID = strawberry.ID
