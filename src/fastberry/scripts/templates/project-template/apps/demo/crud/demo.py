# -*- coding: utf-8 -*-
"""API - Type(Schema) CRUD"""

# Fastberry
from fastberry import CRUD, Settings

# Global Settings
settings = Settings()

# Models
AppModel = lambda: settings.models.get("app_name.model")

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
            return "Detail"

        async def update(info) -> str:
            """Read the Docs"""
            print(info)
            return "Detail"

        async def delete(info) -> str:
            """Read the Docs"""
            print(info)
            return "Detail"
