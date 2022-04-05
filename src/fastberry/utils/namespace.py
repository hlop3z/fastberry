"""
    Nested - SimpleNamespace
"""

import types


class SimpleNamespace(types.SimpleNamespace):
    """Use to create a Nested-Namespace => SimpleNamespace"""

    @staticmethod
    def map_entry(entry):
        """Map-Entry"""
        if isinstance(entry, dict):
            return SimpleNamespace(**entry)
        return entry

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, val in kwargs.items():
            if isinstance(val, dict):
                setattr(self, key, SimpleNamespace(**val))
            elif isinstance(val, list):
                setattr(self, key, list(map(self.map_entry, val)))
