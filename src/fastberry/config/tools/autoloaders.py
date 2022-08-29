""" Fastberry Auto-Loader

    # Collect & Load
    ------------------------------
        ## Core
            - paths         : Project Paths
            - modules       : Project Modules

        ## Click
            - commands      : API Commands

        ## FastAPI
            - middleware    : FastAPI Middleware
            - on_startup    : FastAPI ON_STARTUP
            - on_shutdown   : FastAPI ON_SHUTDOWN
            - router        : FastAPI Routers

        ## GraphQL(strawberry)
        - graphql           : Query(s) & Mutation(s)
        - extensions        : GraphQL Extensions
        - operations        : GraphQL Operations (Aka: Python Resolvers)
"""
import dataclasses as dc
import pathlib
import typing

import dbcontroller as dbc
from fastapi.routing import APIRouter

from ...utils.objects import get_attr, get_fields
from ..extras.click import is_click
from ..extras.strawberry import process_strawberry_crud
from ..imports import import_modules, search_method

YAML = typing.TypeVar("YAML", object, dict, list, None)
METHOD = typing.TypeVar("METHOD", object, dict, list, None)


@dc.dataclass
class ApiPagination:
    """API Pagination"""

    page: int = 1
    limit: int = 100


@dc.dataclass
class EventsExtensions:
    """API Events-Extensions"""

    startup: list = dc.field(default_factory=list)
    shutdown: list = dc.field(default_factory=list)


@dc.dataclass
class ApiGraphQLSchema:
    """API GraphQL Schema"""

    Query: list = dc.field(default_factory=list)
    Mutation: list = dc.field(default_factory=list)


@dc.dataclass
class ApiGraphQLOperations:
    """API Real Methods"""

    query: list = dc.field(default_factory=list)
    mutation: list = dc.field(default_factory=list)


@dc.dataclass
class ApiManager:
    """Fastberry Core Manager"""

    # Core
    modules: list = dc.field(default_factory=list)
    paths: list = dc.field(default_factory=list)
    types: dict = dc.field(default_factory=dict)
    # Pagination
    pagination: METHOD | None = dc.field(default=None)
    # CLI
    all_clis: list = dc.field(default_factory=list)
    # FastAPI
    routers: list = dc.field(default_factory=list)
    add_middleware: METHOD | None = dc.field(default=None)
    events_extensions: EventsExtensions = dc.field(default_factory=EventsExtensions)
    # GraphQL
    schema: ApiGraphQLSchema = dc.field(default_factory=ApiGraphQLSchema)
    operations: ApiGraphQLOperations = dc.field(default_factory=ApiGraphQLOperations)
    graphql_extensions: list = dc.field(default_factory=list)


def load_all_modules(env_mode: str = None, core: YAML = None, is_cli: bool = False):
    """Load ALL Modules"""
    # Merge Apps (Installed + Development)
    installed_apps = core.__dict__.get("installed_apps", [])
    if env_mode == "development":
        development_apps = core.__dict__.get("development_apps", [])
        if development_apps:
            installed_apps.extend(development_apps)

    # Auto-Load Modules
    routers = []
    modules = {}
    all_clis = set()
    gql_schema = {"Query": [], "Mutation": []}
    gql_field_names = {"query": [], "mutation": []}
    gql_paths = set()

    # IF Found Apps
    if installed_apps:
        modules = import_modules(installed_apps)
        for app_name, app_module in modules.items():
            # types = get_attr(app_module, "types")
            if app_name.endswith(".types"):
                for possible_type in get_fields(app_module):
                    current_type = get_attr(app_module, possible_type)
                    if hasattr(current_type, "__meta__"):
                        if hasattr(current_type.__meta__, "is_super_class"):
                            if current_type.__meta__.is_super_class:
                                dbc.Admin.register(current_type)
            elif app_name.endswith(".graphql"):
                # Load CRUD(Query, Mutation)
                gql_types = process_strawberry_crud(app_module)
                gql_schema["Query"].extend(gql_types["Query"])
                gql_schema["Mutation"].extend(gql_types["Mutation"])
                gql_field_names["query"].extend(gql_types["Operations"]["Query"])
                gql_field_names["mutation"].extend(gql_types["Operations"]["Mutation"])
                # Load Operations Folders <Dirs>
                gql_path = pathlib.Path(app_module.__file__).parents[0]
                if gql_path.name == "crud":
                    gql_path = gql_path.parents[0]
                gql_paths.add(gql_path)
            elif app_name.endswith(".router"):
                router = get_attr(app_module, "router")
                # Load Routers
                if isinstance(router, APIRouter):
                    routers.append(router)
                    # self.router.include_router(router)
            elif app_name.endswith(".commands") and is_cli:
                # Load Commands
                cli = get_attr(app_module, "cli")
                if is_click(cli):
                    all_clis.add(cli)

    # Collect Middleware
    installed_middleware = []
    for middleware in core.__dict__.get("middleware") or []:
        current_method = search_method(middleware)
        if current_method:
            installed_middleware.append(current_method)

    # Collect Extensions
    graphql_extensions = []
    for extension in core.__dict__.get("extensions") or []:
        current = search_method(extension)
        if current:
            graphql_extensions.append(current)

    # EVENTS
    events_extensions = {
        "startup": [],
        "shutdown": [],
    }
    for func in core.__dict__.get("on_startup") or []:
        current = search_method(func)
        if current:
            events_extensions["startup"].append(current)
    for func in core.__dict__.get("on_shutdown") or []:
        current = search_method(func)
        if current:
            events_extensions["shutdown"].append(current)

    # Pagination
    items_per_page = core.querying.get("items_per_page", 50)

    def pagination(page: int = 0, limit: int = 100):
        if not page:
            page = 1
        if not limit:
            limit = items_per_page
        limit = min(items_per_page, limit)
        page = min(1, page)
        return ApiPagination(page=page, limit=limit)

    # Install Middleware
    def add_middleware(app):
        """Actually Install The Middleware"""
        for middleware in reversed(installed_middleware):
            app.add_middleware(middleware)
        return app

    # Load Lazy SQL Objects
    dbc.Admin.load()

    # Easy-to-Use Apps
    return ApiManager(
        # Core
        paths=gql_paths,
        modules=modules,
        pagination=pagination,
        # Click
        all_clis=list(all_clis),
        ## FastAPI
        add_middleware=add_middleware,
        events_extensions=EventsExtensions(**events_extensions),
        routers=routers,
        ## GraphQL
        types=dbc.Admin.types,
        graphql_extensions=graphql_extensions,
        schema=ApiGraphQLSchema(**gql_schema),
        operations=ApiGraphQLOperations(**gql_field_names),
    )
