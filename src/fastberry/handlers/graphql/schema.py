"""
    Pre-Schema
"""

import strawberry
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.extensions import AddValidationRules, QueryDepthLimiter


def Schema(
    query: object = None,
    mutation: object | None = None,
    extensions: list | None = None,
    max_depth: int = 4,
    introspection: bool = True,
    **kwargs
) -> strawberry.Schema | None:
    """Strawberry Schema Wrapper"""

    query = query or []
    mutation = mutation or []
    extensions = extensions or []

    Extensions = [
        QueryDepthLimiter(max_depth=max_depth),
    ]
    Extensions.extend(extensions)

    # Apps Extensions
    # settings = Settings()
    # if len(settings.extensions) > 0:
    # Extensions.extend(settings.extensions)

    # Introspection
    if not introspection:
        Extensions.append(AddValidationRules([NoSchemaIntrospectionCustomRule]))

    # Query & Mutation
    items = {}
    if query:
        items["query"] = query
    if mutation:
        items["mutation"] = mutation

    # Return Value
    if query:
        return strawberry.Schema(**items, extensions=Extensions, **kwargs)
    return None
