"""
    Object-Class Tools
"""


def get_fields(model: object):
    """Get Object Fields"""
    return [i for i in dir(model) if not i.startswith("__")]


def get_attr(model: object, name: str):
    """Get Object Attribute IF Exist"""
    if hasattr(model, name):
        return getattr(model, name)
    return None


class Singleton:
    """Create a Singleton"""

    def __new__(cls, *args, **kwargs):
        it_id = "__it__"
        it = cls.__dict__.get(it_id, None)
        if it is not None:
            return it
        it = object.__new__(cls)
        setattr(cls, it_id, it)
        it.init(*args, **kwargs)
        return it

    def init(self, *args, **kwargs):
        """Class __init__ Replacement"""
