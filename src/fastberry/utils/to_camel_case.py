"""
    Converts to Camel-Case
"""


def to_camel_case(text):
    """Converts to Camel-Case"""
    init, *temp = text.split("_")
    return "".join([init.lower(), *map(str.title, temp)])
