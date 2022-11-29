"""
    <Regular> to <Async>
"""

import asyncio
from functools import wraps


def coro(f):
    """Transform <Regular> Function to <Async> Function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        """Wraps the Function"""
        return asyncio.run(f(*args, **kwargs))

    return wrapper
