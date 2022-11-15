"""
    { Controller } for the Database(s)
"""
import fastberry as fb

from . import types


class Base:
    @classmethod
    async def all(cls):
        return await cls.objects.all()

    @classmethod
    async def reset(cls):
        return await cls.objects.delete(None, all=True)


@fb.manager
class Category(Base):
    model = types.Category

    @classmethod
    async def create(cls, form):
        data = form.data
        results = await cls.objects.create(data.__dict__)
        return results
