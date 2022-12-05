# -*- coding: utf-8 -*-
"""
    API - GraphQL
"""

# Fastberry
import fastberry as fb

# Type(s) Tools
from .. import forms, manager, types

# Create your API (GraphQL) here.
@fb.gql
class Todo:
    """Todo Api"""

    class Meta:
        """Meta-Data"""

        app = False
        model = None

    class Query:
        """Query"""

        async def search(status: str | None = None) -> fb.edges(types.Task):
            """Search for task(s) by status"""
            return await manager.Task.search(status)

        async def detail(item: fb.ID) -> fb.query(types.Task):
            """Get task by ID"""
            return await manager.Task.detail(item)

    class Mutation:
        """Mutation"""

        async def create(form: forms.Task) -> fb.mutation(types.Task):
            """Create a new task"""
            return await manager.Task.create(form.input)

        async def update(item: fb.ID, status: str) -> fb.mutation(types.Task):
            """Change task's status"""
            return await manager.Task.update(item, status)

        async def delete(item: fb.ID) -> bool:
            """Delete task by ID"""
            return await manager.Task.delete(item)
