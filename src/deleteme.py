# -*- coding: utf-8 -*-
"""
    API - CRUD
"""

# Fastberry
from fastberry import CRUD


# Create your API (GraphQL) here.
class Demo(CRUD):
    """Demo Api"""

    class Query:
        """Query"""

        async def detail(info) -> str:
            """Read the Docs"""
            print(info)
            return "Detail"

    class Mutation:
        """Mutation"""

        async def create(info) -> str:
            """Read the Docs"""
            print(info)
            return "Create"
