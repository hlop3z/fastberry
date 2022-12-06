"""
    Types
"""

try:
    import dbcontroller as dbc
except ImportError:
    dbc = None


def types(models: list):
    """Collect (GraphQL) Return-Types"""
    single_name: dict = {}
    all_types: dict = {}
    if dbc:
        for active in models:
            is_component = dbc.is_model(active.object)
            if is_component:
                if hasattr(active.object, "__database__"):
                    name = active.object.__name__
                    found = single_name.get(name)
                    if found and found.object != active.object:
                        msg = f"""\n* <Type: { found.name }> is already in use by the <App: { found.app }>"""
                        msg += """\n* <Types> must have UNIQUE names."""
                        msg += f"""\n* Rename it in either <App: { found.app } or { active.app }>."""
                        raise ValueError(msg)
                    single_name[name] = active
                    if callable(active.object.__database__):
                        active.object.__database__()
                    all_types[active.key] = active.object
    return all_types
