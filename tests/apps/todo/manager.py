# -*- coding: utf-8 -*-
"""
    { Controller } for the Database(s)
"""

import fastberry as fb

from . import types

# Create your <managers> here.
@fb.manager
class Task:
    """Task's Database Manager"""

    model = types.Task

    @classmethod
    async def create(cls, form):
        """Create"""
        # Errors
        errors_messages = []

        # Good Input
        if form.is_valid:
            results = await cls.objects.create(
                {
                    "title": form.data.title,
                    "status": form.data.status,
                    "description": form.data.description,
                }
            )
            if not results.error:
                item = results.data
                return types.Task(
                    _id=item._id,
                    id=item.id,
                    title=item.title,
                    status=item.status,
                    description=item.description,
                )

        # Bad Input
        errors_messages.append(fb.error(type="input", text="Something Went Wrong!"))
        return fb.errors(messages=errors_messages)

    @classmethod
    async def update(cls, unique_id, status):
        """Update"""
        # Errors
        errors_messages = []

        # Good Input
        form = {
            "status": status,
        }
        results = await cls.objects.update(unique_id, form)
        if not results.error:
            item = results.data
            return types.Task(
                _id=item._id,
                id=item.id,
                title=item.title,
                status=item.status,
                description=item.description,
            )

        # Bad Input
        errors_messages.append(fb.error(type="input", text="Something Went Wrong!"))
        return fb.errors(messages=errors_messages)

    @classmethod
    async def delete(cls, unique_id):
        """Delete"""
        results = await cls.objects.delete(unique_id)
        if not results.error:
            return True
        return False

    @classmethod
    async def detail(cls, unique_id):
        """Detail"""
        results = await cls.objects.detail(unique_id)
        return results

    @classmethod
    async def search(cls, search=None):
        """Search"""
        columns = ["status"]
        results = await cls.objects.search(
            columns=columns, value=search, page=1, limit=100, sort_by="-id"
        )
        # Search
        if not results.error:
            return fb.page(
                edges=[
                    types.Task(
                        _id=item._id,
                        id=item.id,
                        title=item.title,
                        status=item.status,
                        description=item.description,
                    )
                    for item in results.data
                ],
                length=results.count,
                pages=results.pages,
            )
        # All Items
        return fb.page(
            edges=[],
            length=0,
            pages=0,
        )
