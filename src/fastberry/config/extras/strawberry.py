"""Get App(s) Methods

Declared as <Query> or <Mutation>.
Each method is grouped by one of the two category.

methods:
    process_strawberry_crud: Collect App Methods.
"""

from ...utils.objects import get_attr, get_fields
from .crud import is_crud


def process_strawberry_crud(app_module):
    """Strawberry C.R.U.D"""

    gql_schema = {
        "Query": [],
        "Mutation": [],
        "Operations": {"Query": [], "Mutation": []},
    }
    for crud_name in get_fields(app_module):
        crud_module = getattr(app_module, crud_name)
        # CRUD
        if is_crud(crud_module):
            for field in [
                "Query",
                "Mutation",
            ]:
                op_class = get_attr(crud_module, field)
                op_fields = get_fields(op_class)
                for op in op_fields:
                    op_method = get_attr(op_class, op)
                    setattr(op_class, op, staticmethod(op_method))
                if op_class:
                    setattr(op_class, "keys", op_fields)
            # Init class and add all (Queries & Mutations)
            crud = crud_module()
            gql_query = get_attr(crud, "Query")
            gql_mutation = get_attr(crud, "Mutation")
            gql_names = get_attr(crud, "Operations")
            # Operations-Names
            gql_schema["Operations"]["Query"].extend(gql_names["Query"])
            gql_schema["Operations"]["Mutation"].extend(gql_names["Mutation"])
            # Items or None
            if gql_query:
                gql_schema["Query"].append(gql_query)
            if gql_mutation:
                gql_schema["Mutation"].append(gql_mutation)
    return gql_schema
