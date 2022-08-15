"""C.R.U.D Base

classes:
    GQL: The base for GraphQL (Query & Mutation) methods.

methods:
    is_crud: Check if value is a subclass ot <CRUD>.
"""

import strawberry
from strawberry.types import Info

from ...utils.objects import Singleton, get_attr
from .. import core
from ..imports import search_method


def api_name(self):
    """API Name Maker"""

    if self.name:
        return f"{self.name}API"
    return "API"


def is_crud(crud):
    """Check if item is subclass of <GQL>"""

    its_crud = False
    try:
        if not crud == GQL:
            its_crud = issubclass(crud, GQL)
    except TypeError:
        pass
    return its_crud


class GQL(Singleton):
    """CRUD (GraphQL) Singleton"""

    def init(self):
        """__init__ Only Runs Once Per Class."""

        settings = core.Settings()

        permission_classes = []
        for perm in settings.base.__dict__.get("permissions") or []:
            permission = search_method(perm)
            if permission:
                permission_classes.append(permission)

        try:
            self.name = self.schema.__name__
        except AttributeError:
            self.name = None

        app_prefix = get_attr(self, "prefix")
        all_mutation = get_attr(self, "Mutation")
        all_query = get_attr(self, "Query")

        dict_names = {"Query": [], "Mutation": []}
        dict_mutation = {}
        dict_query = {}

        if isinstance(app_prefix, str):
            app_prefix = app_prefix.lower()

        # Naming
        def func_name(key, group=self.name, prefix=app_prefix):
            """Create the function's name."""
            if group:
                schema_name = group.lower()
                return_value = f"{schema_name}_{key.lower()}"
            else:
                return_value = key.lower()
            if prefix:
                return_value = f"{prefix}_{return_value}"
            return return_value

        # Mutation
        if hasattr(all_mutation, "keys"):
            for key in all_mutation.keys:
                resolver_name = func_name(key)
                resolver_func = get_attr(all_mutation, key)
                resolver_func.__annotations__["info"] = Info
                dict_names["Mutation"].append(resolver_name)
                dict_mutation[resolver_name] = strawberry.field(
                    resolver=resolver_func,
                    description=(resolver_func.__doc__ or "").strip(),
                    permission_classes=permission_classes,
                )

        # Query
        if hasattr(all_query, "keys"):
            for key in all_query.keys:
                resolver_name = func_name(key)
                resolver_func = get_attr(all_query, key)
                resolver_func.__annotations__["info"] = Info
                dict_names["Query"].append(resolver_name)
                dict_query[resolver_name] = strawberry.field(
                    resolver=resolver_func,
                    description=(resolver_func.__doc__ or "").strip(),
                    permission_classes=permission_classes,
                )

        # Names
        self.Operations = dict_names

        # Write
        self.Mutation = None
        if dict_mutation:
            self.Mutation = strawberry.type(
                type(
                    api_name(self),
                    (object,),
                    dict_mutation,
                )
            )

        # Read
        self.Query = None
        if dict_query:
            self.Query = strawberry.type(
                type(
                    api_name(self),
                    (object,),
                    dict_query,
                )
            )
