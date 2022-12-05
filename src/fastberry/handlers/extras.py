"""
    Extras [middleware, on_startup, on_shutdown, extensions, permissions]
"""
import functools

from ..core import types


def add_middleware(app=None, installed: list = None):
    """Install The Middleware"""
    for middleware in reversed(installed):
        app.add_middleware(middleware)
    return app


def extras(items):
    """Collect Extras From (`spoc.toml`)"""
    extra_out = dict(items)
    extra_out["middleware"] = functools.partial(
        add_middleware, installed=extra_out.get("middleware", {})
    )
    return types.Extras(**extra_out)
