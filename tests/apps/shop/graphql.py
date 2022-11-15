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

        async def detail(item: fb.item) -> fb.query(types.Category):
            """(Detail-Operation) Read The Docs"""

            return types.Category(_id=1, id="$encoded_id$", name="Cool")

        async def search(
            search: forms.Search, pagination: fb.pagination
        ) -> fb.edges(types.Category):
            """(Search-Operation) Read The Docs"""

            # Do Something if input { IS VALID } ...
            if search.input.is_valid:
                print("\n# Client's Inputs #")
                print(search.input.data)
                print(pagination.input.data)

            # Get Data from the { Database } ...
            results = await manager.Category.all()
            print("\n# Database Response #")
            print(results)

            # Return { Page }
            return fb.page(
                edges=[
                    types.Category(_id=1, id=1, name="Computer"),
                    types.Category(_id=2, id=2, name="Radio"),
                ],
                length=2,
                pages=1,
            )

    class Mutation:
        """GraphQL Mutation"""

        async def create(form: forms.Category) -> fb.mutation(types.Category):
            """(Create-Operation) Read The Docs"""

            # Client's Input
            if form.input.is_valid:
                print(form.input.data)

            # Errors
            errors_messages = []

            # IF error . . .
            errors_messages.append(fb.error(type="input", text="Error for Demo!"))
            return fb.errors(messages=errors_messages)
