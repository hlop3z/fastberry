"""
    [GraphQL-Tools]
"""

from .client import build_client
from .reader import get_info

INTROSPECTION_QUERY = """
{
  __schema {
    mutation: mutationType {
      name
      fields {
        name
      }
    }
    query: queryType {
      name
      fields {
        name
      }
    }
  }
}
"""


def introspection_info(schema):
    """GraphQL Introspection INFO"""
    result = schema.execute_sync(INTROSPECTION_QUERY)
    return get_info(result.data)
