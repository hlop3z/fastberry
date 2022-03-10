from dataclasses import field
from typing import Generic, TypeVar

import strawberry

from fastberry.graphql.typing import Dict

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
    extra: Dict = field(default_factory=dict)


@strawberry.type
class Edge(Generic[GenericType]):
    """An edge may contain additional information of the relationship. This is the trivial case"""

    node: GenericType
    cursor: str


class Response:
    def __init__(self):
        self.__edges = []

    def add(self, item):
        edge = Edge(node=item, cursor=item.id)
        self.__edges.append(edge)

    def __call__(self, length: int = None, pages: int = None, extra: dict = {}):
        edges = self.__edges
        if len(edges) > 0:
            return Connection(
                page_info=PageInfo(
                    length=length,
                    pages=pages,
                    extra=extra,
                ),
                edges=edges,
            )
        return None
