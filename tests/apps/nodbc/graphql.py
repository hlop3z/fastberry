"""
    { Operations } for GraphQL
"""
import fastberry as fb

from . import forms, manager, types


@fb.gql
class Demo:
    """GraphQL Manager"""

    class Meta:
        """Class Meta-Data"""

        app = False
        model = "Category"

    class Query:
        """GraphQL Query"""

        async def detail(item: str) -> fb.query(types.Category):
            """(Detail-Operation) Read The Docs"""

            return types.Category(name="Cool")
