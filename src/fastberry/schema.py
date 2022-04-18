"""
    Pre-Schema
"""

import strawberry
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.extensions import AddValidationRules, QueryDepthLimiter
from strawberry.tools import merge_types

from .config import Settings


def Schema(
    query: list = None,
    mutation: list = None,
    extensions: list = None,
    max_depth: int = 4,
    introspection: bool = True,
    **kwargs
) -> strawberry.Schema | None:
    """Strawberry Schema Wrapper"""

    query = query or []
    mutation = mutation or []
    extensions = extensions or []

    Query = tuple(query)
    Mutation = tuple(mutation)
    Extensions = [
        QueryDepthLimiter(max_depth=max_depth),
    ]
    Extensions.extend(extensions)

    # Apps Extensions
    settings = Settings()
    if len(settings.extensions) > 0:
        Extensions.extend(settings.extensions)

    # Introspection
    if not introspection:
        Extensions.append(AddValidationRules([NoSchemaIntrospectionCustomRule]))

    # Query & Mutation
    items = {}
    if Query:
        items["query"] = merge_types("Query", Query)
    if Mutation:
        items["mutation"] = merge_types("Mutation", Mutation)

    # Return Value
    if Query:
        return strawberry.Schema(**items, extensions=Extensions, **kwargs)
    return None
