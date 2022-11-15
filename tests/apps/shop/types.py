"""
    { Types } for GraphQL
"""
from typing import Optional

import fastberry as fb

@fb.sql.model
class Category:
    """(Type) Read The Docs"""

    name: str