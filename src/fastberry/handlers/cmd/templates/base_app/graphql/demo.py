# -*- coding: utf-8 -*-
"""
    API - GraphQL
"""

# Fastberry
import fastberry as fb

# Create your API (GraphQL) here.
@fb.gql
class Demo:
    """Demo Api"""

    class Meta:
        """Meta-Data"""

        app = False
        model = None

    class Query:
        """Query"""

        async def search(info, pagination: fb.pagination) -> str:
            """Read the Docs"""
            print(info)
            print(pagination.input)
            return "Search"

        async def detail(info, item: fb.item) -> str:
            """Read the Docs"""
            print(info)
            print(item.input)
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
