import fastberry as fb

try:
    import dbcontroller as dbc

    form = dbc.form.graphql
    value = dbc.form.field
    ID = dbc.ID
except ImportError:

    dbc = False


if dbc:
    core = form()

    ITEM_DOC = """
    Global **Selector** for **ITEM(s)** by **ID(s)**.
    """

    PAGINATION_DOC = """
    Global **Pagination**

    **Setting**: `(all: true)` 

    **Returns**: **All** of the **items** in the **Database** (Mostly For **Admin(s) Use Only**).
    """

    @core(description=ITEM_DOC)
    class Item:
        """
        Item
        """

        id = value(
            ID,
            default=None,
        )
        ids = value(
            list[ID],
            default=None,
        )

        class Next:
            """Run After User-Input"""

            def run(self):
                """Run"""
                self.is_list = False
                if self.id is None and self.ids is not None:
                    self.is_list = True

    @core(description=PAGINATION_DOC)
    class Pagination:
        """
        Pagination
        """

        limit = value(
            int,
            default=10,
        )
        page = value(
            int,
            default=10,
        )
        sort_by = value(
            str,
            default="-id",
        )
        all = value(
            bool,
            default=False,
        )

        class Next:
            """Run After User-Input"""

            def run(self):
                """Run"""
                controller = fb.App()
                page = controller.pagination(
                    page=self.page,
                    limit=self.limit,
                )
                self.page = page.page
                self.limit = page.limit

else:
    Item = type("Item", (object,), {})
    Pagination = type("Pagination", (object,), {})
