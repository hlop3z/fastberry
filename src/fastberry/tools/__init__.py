"""
    Tool to Transform { Text } to { Code-Cases }
    Tool to Get Module's Name
"""
import re

from .coro import coro
from .forms import Item, Pagination


def doc(description):
    """Inject Documentation"""

    def decorator(function):
        """Decorator"""
        function.__doc__ = description
        return function

    return decorator


def to_kebab_case(text):
    """Clean Text"""
    text = re.sub("[^0-9a-zA-Z]+", "-", str(text))
    return text.lower()


def to_camel_case(text):
    """Converts to { camelCase }"""
    text = to_kebab_case(text)
    init, *temp = text.title().split("-")
    return "".join([init.lower()] + temp)


def to_pascal_case(text):
    """Converts to { PascalCase }"""
    text = to_kebab_case(text)
    return text.title().replace("-", "")
