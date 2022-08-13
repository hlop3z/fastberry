"""
    Strawberry Pagination
"""

import typing

import strawberry

from ..config import Settings

settings = Settings()

try:
    ITEMS_PER_PAGE = settings.base.querying.get("items_per_page")
except:
    ITEMS_PER_PAGE = 50


@strawberry.input
class Pagination:
    """GraphQL Pagination"""

    page: int = 1
    limit: typing.Optional[int] = ITEMS_PER_PAGE
    sort_by: typing.Optional[str] = "-id"
    all: typing.Optional[bool] = False

    def init(self):
        """Add Search Parameters to Query"""
        page = settings.apps.pagination(
            page=self.page,
            limit=self.limit,
        )
        if self.sort_by == "-id":
            sort_by = "-_id"
        elif self.sort_by == "id":
            sort_by = "_id"
        else:
            sort_by = self.sort_by
        return Pagination(
            page=page.page,
            limit=page.limit,
            sort_by=sort_by,
            all=self.all,
        )
