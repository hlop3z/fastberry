"""
    GraphQL - Strawberry
"""
import functools
import typing
from collections import namedtuple

import spoc
import strawberry
from strawberry.types import Info

from ...components import COMPONENT
from .schema import Schema

GraphQL = namedtuple("GraphQL", ["schema", "info", "operations"])
GraphQLInfo = namedtuple("Info", ["query", "mutation"])
Operation = namedtuple("Operation", ["name", "annotations"])


def operation_annotations(annotations: dict):
    """GraphQL Operations"""
    ops_annotations = {"inputs": {}}
    for key, val in annotations:
        if key == "return":
            return_types = set()
            for item in typing.get_args(val):
                if hasattr(item, "__name__"):  # hasattr(item, "__spoc__") and
                    return_types.add(item.__name__)
            ops_annotations["return"] = list(return_types)
        else:
            if hasattr(val, "__spoc__") and hasattr(val, "__name__"):
                ops_annotations["inputs"][key] = val.__name__
    return ops_annotations


def create_operation(name, annotations):
    """Create Operations NamedTuple"""
    return Operation(
        name=name,
        annotations=operation_annotations(annotations.items()),
    )


def create_name(method: object, app: str = None, model: str = None):
    """GraphQL Resolver's Name"""
    if model:
        method_name = f"{model}_{method.__name__}"
    else:
        method_name = method.__name__
    if app:
        method_name = f"{app}_{method_name}"
    return method_name


def get_module_name(model: object):
    """Get: Class-Module's Name"""
    name = model.__module__
    parts = name.split(".")
    if parts[0] == "apps" and len(parts) > 1:
        parts.pop(0)
    module_name = parts[0]
    if module_name == "__main__":
        module_name = "main"
    return module_name


def graphql(schemas: list = None, permissions: list = None):
    """Collect (GraphQL) Strawberry"""
    gql_schema = {"Query": {}, "Mutation": {}}
    permission_classes = permissions or []
    fastberry_operations = []
    # Collect
    for active in schemas:
        is_component = spoc.is_component(active.object, COMPONENT["graphql"])
        if is_component:
            cls_fields = spoc.get_fields(active.object)
            method_model = None
            method_app = get_module_name(active.object)
            if hasattr(active.object, "Meta"):
                if hasattr(active.object.Meta, "model"):
                    method_model = getattr(active.object.Meta, "model")
                if hasattr(active.object.Meta, "app"):
                    method_app = getattr(active.object.Meta, "app")
            if "Query" in cls_fields:
                cls_query = getattr(active.object, "Query")
                cls_query_fields = spoc.get_fields(cls_query)
                for current in cls_query_fields:
                    resolver_func = getattr(cls_query, current)
                    resolver_name = create_name(
                        resolver_func, app=method_app, model=method_model
                    )
                    op = functools.partial(
                        create_operation, resolver_name, resolver_func.__annotations__
                    )
                    fastberry_operations.append(op)
                    resolver_func.__annotations__["info"] = Info
                    gql_schema["Query"][resolver_name] = strawberry.field(
                        resolver=resolver_func,
                        description=(resolver_func.__doc__ or "").strip(),
                        permission_classes=permission_classes,
                    )
            if "Mutation" in cls_fields:
                cls_query = getattr(active.object, "Mutation")
                cls_query_fields = spoc.get_fields(cls_query)
                for current in cls_query_fields:
                    resolver_func = getattr(cls_query, current)
                    resolver_name = create_name(
                        resolver_func, app=method_app, model=method_model
                    )
                    op = functools.partial(
                        create_operation, resolver_name, resolver_func.__annotations__
                    )
                    fastberry_operations.append(op)
                    resolver_func.__annotations__["info"] = Info
                    gql_schema["Mutation"][resolver_name] = strawberry.field(
                        resolver=resolver_func,
                        description=(resolver_func.__doc__ or "").strip(),
                        permission_classes=permission_classes,
                    )
    # Build Schema
    Query = None
    Mutation = None
    if gql_schema["Query"]:
        Query = type("Query", (object,), gql_schema["Query"])
        Query = strawberry.type(Query)
    if gql_schema["Mutation"]:
        Mutation = type("Mutation", (object,), gql_schema["Mutation"])
        Mutation = strawberry.type(Mutation)
    return GraphQL(
        operations=fastberry_operations,
        schema=functools.partial(Schema, query=Query, mutation=Mutation),
        info=GraphQLInfo(
            query=frozenset(gql_schema["Query"].keys()),
            mutation=frozenset(gql_schema["Mutation"].keys()),
        ),
    )
