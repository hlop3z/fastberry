"""
    Pre-Schema
"""

import strawberry
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.extensions import AddValidationRules, QueryDepthLimiter
from strawberry.tools import merge_types


def Schema(
    query: list = None,
    mutation: list = None,
    extensions: list = None,
    max_depth: int = 4,
    introspection: bool = True,
    **kwargs
) -> strawberry.Schema:
    """Strawberry Schema Wrapper"""

    query = query or []
    mutation = mutation or []
    extensions = extensions or []

    Query = tuple(query)
    Mutation = tuple(mutation)

    # Extension
    Extensions = [
        QueryDepthLimiter(max_depth=max_depth),
    ]
    Extensions.extend(extensions)

    # Introspection
    if not introspection:
        Extensions.append(AddValidationRules([NoSchemaIntrospectionCustomRule]))

    items = {}
    if Query:
        items["query"] = merge_types("Query", Query)
    if Mutation:
        items["mutation"] = merge_types("Mutation", Mutation)

    # Return Value
    return strawberry.Schema(**items, extensions=Extensions, **kwargs)
