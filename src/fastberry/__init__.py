"""
    Fastberry Main (Core-Methods)
"""

from starlette.middleware.base import BaseHTTPMiddleware as BaseMiddleware
from strawberry.extensions import Extension as BaseExtension
from strawberry.permission import BasePermission
import strawberry

from . import config

# from .config import Settings
from .config import Settings as Fastberry
from .config.extras.gql import GQL

# from .graphql import BaseType
from .schema import Schema
from .types import Model, SQLFilters

# Custom Field Types
Text = Model.text
JSON = Model.json
ID = strawberry.ID

# To Camel Case
def to_camel_case(text):
    """Converts to Camel-Case"""
    init, *temp = text.split("_")
    return "".join([init.lower(), *map(str.title, temp)])
