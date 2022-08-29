"""
    Strawberry Pagination
"""

import dataclasses as dc
import typing

import strawberry

from ..config import Settings

settings = Settings()

try:
    ITEMS_PER_PAGE = settings.base.querying.get("items_per_page")
except:
    ITEMS_PER_PAGE = 50


@strawberry.input
@dc.dataclass
class Pagination:
    """GraphQL Pagination"""

    page: int = 1
    limit: typing.Optional[int] = ITEMS_PER_PAGE
    sort_by: typing.Optional[str] = "-id"
    all: typing.Optional[bool] = False

    def __post_init__(self):
        """Add Search Parameters to Query"""
        page = settings.apps.pagination(
            page=self.page,
            limit=self.limit,
        )
        self.page = page.page
        self.limit = page.limit
