from dataclasses import field

import strawberry

from .pagination import Connection
from .typing import Dict, List


@strawberry.type
class Error:
    type: str = None
    messages: List = field(default_factory=list)
    meta: Dict = field(default_factory=dict)
    error: bool = True


def Query(Model):
    return Model | None


def Mutation(Model):
    return Model | Error | None


def Edges(Model):
    return Connection[Model] | None
