"""
    DataClass
"""
import dataclasses as dc
import typing


def pagination(toml):
    """Pagination"""
    max_items_per_page: int = toml.get("api", {}).get("items_per_page", 100)

    def init(self):
        page = max(1, self.page)
        limit = min(max_items_per_page, self.limit)
        if page < 0:
            page = 1
        self.page = page
        self.limit = max(limit, max_items_per_page)

    data_class = dc.make_dataclass(
        "Pagination",
        [
            ("page", typing.Optional[int], dc.field(default=1)),
            ("limit", typing.Optional[int], dc.field(default=100)),
        ],
        namespace={"__post_init__": init},
    )
    return data_class
