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


class Demo(GQL):
    """Demo Api"""

    class Query:
        """Query"""

        async def detail() -> Query(types.Product):
            return types.Product(name="Model", aliases=["type", "class", "object"])

        async def single_instance(
            search: str | None = None
        ) -> Query(types.Author):
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
