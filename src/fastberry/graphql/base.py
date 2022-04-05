"""
    Strawberry BaseType
"""

import strawberry


@strawberry.type
class BaseType:
    """GrahpQL Base-Type"""

    id: strawberry.ID
    _id: str
