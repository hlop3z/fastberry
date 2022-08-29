# -*- coding: utf-8 -*-
"""
    API - CRUD
"""

from fastberry import GQL
from fastberry.graphql.inputs import Pagination
from fastberry.graphql.types import (
    Edges,
    Error,
    ErrorMessage,
    Mutation,
    Query,
    Response,
)

from .. import types
from ..forms import query

# controller = controller.x.admin([types.Author])
# print(controller)
# result = await controller.Author.all()
# print(result)


class Demo(GQL):
    """Demo Api"""

    class Query:
        """Query"""

        async def detail(search: query.Search) -> Query(types.Product):
            print(search.input)
            return types.Product(name="Model")

        async def single_instance(search: str | None = None) -> Query(types.Author):
            return types.Author(_id=1, id=1, name="Ludwig Van Beethoven")

        async def multiple_instances(
            pagination: Pagination,
        ) -> Edges(types.Author):
            print(pagination)
            return Response(
                edges=[
                    types.Author(_id=1, id=1, name="Ludwig Van Beethoven"),
                    types.Author(_id=2, id=2, name="Wolfgang Amadeus Mozart"),
                ],
                length=2,
                pages=1,
            )

    class Mutation:
        """Mutation"""

        async def create_good() -> Mutation(types.Author):
            if True:
                return types.Author(_id=2, id=2, name="Wolfgang Amadeus Mozart")
            return None

        async def create_bad() -> Mutation(types.Author):
            if False:
                return None
            return Error([ErrorMessage(type="input", message="invalid input.")])


DEMO_DOC = """
```graphql
query MyQuery {
    detail(search: {}) {
        name
        aliases
        stock
        isAvailable
        availableFrom
        createdAt
        sameDayShippingBefore
        price
        notes
        isObject
        isJson
        demo {
            author { name }
            category { name }
        }                        
    }
}
```
"""

Demo.Query.detail.__doc__ = DEMO_DOC
