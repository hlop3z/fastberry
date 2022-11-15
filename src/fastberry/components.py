"""
    Components
"""
import functools

import click
from fastapi import APIRouter

import spoc

COMPONENT = {}
COMPONENT["graphql"] = {"engine": "strawberry-graphql", "type": "schema"}
COMPONENT["router"] = {"engine": "fastapi", "type": "router"}
COMPONENT["commands"] = {"engine": "click", "type": "group"}

# Router
spoc.component(APIRouter, metadata=COMPONENT["router"])

# GraphQL Class @Decorator
def graphql(
    cls: object = None,
):
    """Strawberry { GraphQL } Creator"""
    spoc.component(cls, metadata=COMPONENT["graphql"])
    return cls


# Command-Line Interface
def cli(
    cls: object = None,
    *,
    group: bool = False,
):
    """Click { CLI } Creator"""
    if cls is None:
        return functools.partial(
            cli,
            group=group,
        )
    # Real Wrapper
    cls = click.group(cls)
    if not group:
        spoc.component(cls, metadata=COMPONENT["commands"])
    return cls
