# -*- coding: utf-8 -*-
"""
    API - CRUD
"""

# Fastberry
from fastberry import GQL

from .. import types


# Create your API (GraphQL) here.
class Demo(GQL):
    """Demo Api"""

    class Query:
        """Query"""

        async def detail() -> types.Note:
            return types.Note(name="My Note", text="Hello World")

    class Mutation:
        """Mutation"""

        async def create(
            name: str = "My Note", text: str = "Hello World"
        ) -> types.Note:
            return types.Note(name=name, text=text)
