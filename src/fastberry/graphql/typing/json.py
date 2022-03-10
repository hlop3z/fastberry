import json
from typing import Any, NewType

import strawberry


def load_list(v):
    val = json.loads(v)
    return val if isinstance(val, list) else []


def load_dict(v):
    val = json.loads(v)
    return val if isinstance(val, dict) else {}


JSONScalar = strawberry.scalar(
    NewType("JSON", Any),
    serialize=lambda v: v,
    parse_value=lambda v: json.loads(v),
    description="The JSON scalar type represents a generic GraphQL scalar value that could be: <Array or Object>.",
)

ListScalar = strawberry.scalar(
    NewType("List", Any),
    serialize=lambda v: v,
    parse_value=lambda v: load_list(v),
    description="The List scalar type represents a generic GraphQL scalar value that could be: <List or Array>.",
)

DictScalar = strawberry.scalar(
    NewType("Dict", Any),
    serialize=lambda v: v,
    parse_value=lambda v: load_dict(v),
    description="The Dict scalar type represents a generic GraphQL scalar value that could be: <Dict or Object>.",
)
