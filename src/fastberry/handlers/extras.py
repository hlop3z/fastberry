"""
    Extras [middleware, on_startup, on_shutdown, extensions, permissions]
"""
import functools
from typing import Any

from ..core import types


def add_middleware(app: Any = None, installed: list | None = None):
    """Install The Middleware"""
    installed = installed or []
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
