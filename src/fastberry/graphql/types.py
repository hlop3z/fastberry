""" Strawberry - GraphQL (Connection, PageInfo, Edges)
    Made Easy by wrapping functions together.

methods:
    Mutation: GraphQL Mutation.
    Query: GraphQL Query.
    Edges: GraphQL Edges.
    Response: Response GraphQL Edges.
    Error: Response Error([ErrorMessage]).
    ErrorMessage: Error Message.
"""

from dataclasses import field

import strawberry
from strawberry.scalars import JSON

from .edges import Connection, Edge, PageInfo


@strawberry.type
class ErrorMessage:
    """GraphQL Error Message"""

    # ['field', 'type', 'text']

    field: str | None = None
    type: str | None = None
    text: str | None = None


@strawberry.type
class Error:
    """GraphQL Error"""

    messages: list[ErrorMessage] = field(default_factory=list)
    meta: JSON = field(default_factory=dict)
    error: bool = True


def Query(model):
    """GraphQL Query"""
    return model | None


def Mutation(model):
    """GraphQL Mutation"""
    return model | Error


def Edges(model) -> Connection:
    """GraphQL Edges"""
    return Connection[model]


def Page(
    edges: list[Edge] = None, length: int = 0, pages: int = 0, extra: dict = None
) -> Connection:
    """Edges { Page } Response"""
    edges = edges or []
    extra = extra or {}
    items = [Edge(node=item, cursor=item.id) for item in edges]
    return Connection(
        page_info=PageInfo(
            length=length,
            pages=pages,
            extra=extra,
        ),
        edges=items,
    )
