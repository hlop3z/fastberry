"""
    Strawberry - GraphQL (Connection, PageInfo, Edges)
"""

from dataclasses import field
from typing import Generic, TypeVar

import strawberry
from strawberry.scalars import JSON

GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    """Represents a paginated relationship between two entities"""

    page_info: "PageInfo"
    edges: list["Edge[GenericType]"]


@strawberry.type
class PageInfo:
    """Pagination context to navigate objects with cursor-based pagination"""

    length: int
    pages: int
    extra: JSON = field(default_factory=dict)


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str
