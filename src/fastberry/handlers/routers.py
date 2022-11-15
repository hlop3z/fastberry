"""
    Routers
"""
from fastapi import APIRouter


def routers(routers: list):
    """Collect (FastAPI) Routers"""
    router = []
    for active in routers:
        if isinstance(active.object, APIRouter):
            router.append(active.object)
    return router
