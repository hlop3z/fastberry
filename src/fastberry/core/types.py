"""
    DataClass
"""
import dataclasses as dc
import typing


@dc.dataclass(frozen=True)
class FastAPI:
    """FastAPI"""

    title: str
    version: str
    description: typing.Any = None


@dc.dataclass(frozen=True)
class Extras:
    """API Extras"""

    middleware: typing.Any = None
    on_startup: typing.Any = None
    on_shutdown: typing.Any = None
    extensions: typing.Any = None
    permissions: typing.Any = None
