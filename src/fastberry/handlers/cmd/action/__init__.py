""" [Complex-Tools]
"""
from .schema_reader import INTROSPECTION_QUERY, get_info


def introspection_info(schema):
    """GraphQL Introspection INFO"""
    result = schema.execute_sync(INTROSPECTION_QUERY)
    return get_info(result.data)
