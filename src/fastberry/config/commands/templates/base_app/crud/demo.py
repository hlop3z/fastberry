# -*- coding: utf-8 -*-
"""
    API - CRUD
"""

# Fastberry
from fastberry import CRUD

# Create your API (GraphQL) here.
class Demo(CRUD):
    """Demo Api"""

    schema = None
    prefix = "demo"

    class Query:
        """Query"""

        async def search(info) -> str:
            """Read the Docs"""
            print(info)
            return "Search"

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

        async def update(info) -> str:
            """Read the Docs"""
            print(info)
            return "Update"

        async def delete(info) -> str:
            """Read the Docs"""
            print(info)
            return "Delete"
