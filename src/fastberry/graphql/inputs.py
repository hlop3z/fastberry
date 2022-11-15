"""
    Strawberry Pagination
"""

import dataclasses as dc
import typing

import fastberry as fb
import strawberry

DOC = """
**Setting**: `(all: true)` 

**Returns**: **All** of the **items** in the **Database** (Mostly For **Admin(s) Use Only**).
"""


@strawberry.input(description=DOC)
@dc.dataclass
class Pagination:
    """GraphQL Pagination"""

    page: int = 1
    limit: typing.Optional[int] = 50
    sort_by: typing.Optional[str] = "-id"
    all: typing.Optional[bool] = False

    def __post_init__(self):
        """Add Search Parameters to Query"""
        controller = fb.App()
        page = controller.pagination(
            page=self.page,
            limit=self.limit,
        )
        self.page = page.page
        self.limit = page.limit
