"""
    Types
"""

try:
    import dbcontroller as dbc
except ImportError:
    dbc = None


def forms(models: list):
    """Collect (GraphQL) Input-Forms"""
    single_name: dict = {}
    all_forms: dict = {}
    if dbc:
        for active in models:
            is_component = dbc.is_form(active.object)
            if is_component:
                name = active.object.__name__
                found = single_name.get(name)
                if found and found.object != active.object:
                    app = found.app
                    err = f"""\n* <Form: { name }> is already in use by the <App: { app }>"""
                    err += """\n* <Forms> must have UNIQUE names."""
                    err += f"""\n* Rename it in either <App: { app } or { app }>."""
                    raise ValueError(err)
                single_name[name] = active
                all_forms[active.key] = active.object
    return all_forms
