"""
    Routers
"""
from fastapi import APIRouter


def routers(items: list):
    """Collect (FastAPI) Routers"""
    router = []
    for active in items:
        if isinstance(active.object, APIRouter):
            router.append(active.object)
    return router
