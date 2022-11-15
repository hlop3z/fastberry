"""
    { Types } for GraphQL
"""
from typing import Optional

import fastberry as fb


@fb.type
class Category:
    """(Type) Read The Docs"""

    name: str
