""" Fastberry Core

    import pathlib

    # Build paths inside the project like this: BASE_DIR / "subdir".
    BASE_DIR = pathlib.Path(__file__).resolve().parents[1]

    # Or like this: settings.base_dir / "subdir".
    settings = Settings(base_dir=BASE_DIR)

classes:
    Settings: Singleton.
"""

import os
import pathlib
import sys
import types

import click
from fastapi.routing import APIRouter

from ..utils.objects import Singleton, get_attr
from .definitions import load_docs, load_env, load_mode, load_yaml
from .extras.click import command_collection, is_click
from .extras.models import process_models
from .extras.strawberry import process_strawberry_crud
from .imports import import_modules, search_method


class Settings(Singleton):
    """
    # Use it like this in your scripts.
    settings = Settings()
    """

    def init(self, base_dir: pathlib.Path = None, is_cli: bool = False):
        """__init__ Only Runs Once Per Settings Project."""

        if not base_dir:
            raise Exception("Missing: Settings(base_dir=BASE_DIR)")

        # Core
        core = load_yaml()
        env_mode = load_mode().get("mode", "development")
        env = load_env(env_mode)

        # BASE_DIR
        self.base_dir = base_dir

        # Setup
        self.base = core
        self.env = env
        self.docs = load_docs()
        self.mode = env_mode
        self.debug = env.debug
        self.secret_key = env.secret_key
        self.debug = env.debug

        # Router
        router = APIRouter()
        self.router = router

        # Keys
        self.keys = [
            "base_dir",
            "base",
            "docs",
            "mode",
            "debug",
            "secret_key",
            "apps",
        ]

        # Include BASE_DIR / "apps"
        if base_dir:
            sys.path.insert(0, os.path.join(base_dir, "apps"))

        # Merge Apps (Installed + Development)
        installed_apps = core.__dict__.get("installed_apps")
        installed_apps = installed_apps or []
        if env_mode == "development":
            development_apps = core.__dict__.get("development_apps", [])
            development_apps = development_apps or []
            if development_apps:
                installed_apps.extend(development_apps)

        # Auto-Load Modules
        modules = {}
        all_models = {}
        all_clis = set()
        gql_schema = {"Query": [], "Mutation": []}
        gql_field_names = {"query": [], "mutation": []}
        gql_paths = set()

        # IF Found Apps
        if installed_apps:
            modules = import_modules(installed_apps)
            for app_name, app_module in modules.items():
                if app_name.endswith(".crud"):
                    # Load CRUD(Query, Mutation)
                    gql_types = process_strawberry_crud(app_module)
                    gql_schema["Query"].extend(gql_types["Query"])
                    gql_schema["Mutation"].extend(gql_types["Mutation"])
                    gql_field_names["query"].extend(gql_types["Operations"]["Query"])
                    gql_field_names["mutation"].extend(
                        gql_types["Operations"]["Mutation"]
                    )
                    # Load Operations Folders <Dirs>
                    gql_path = pathlib.Path(app_module.__file__).parents[0]
                    if gql_path.name == "crud":
                        gql_path = gql_path.parents[0]
                    gql_paths.add(gql_path)
                elif app_name.endswith(".models"):
                    # Load Model
                    all_models.update(process_models(app_name, app_module))
                elif app_name.endswith(".router"):
                    router = get_attr(app_module, "router")
                    # Load Routers
                    if isinstance(router, APIRouter):
                        self.router.include_router(router)
                elif app_name.endswith(".commands") and is_cli:
                    # Load Commands
                    cli = get_attr(app_module, "cli")
                    if is_click(cli):
                        all_clis.add(cli)

        # Middleware
        installed_middleware = []
        for middleware in core.__dict__.get("middleware") or []:
            current_method = search_method(middleware)
            if current_method:
                installed_middleware.append(current_method)

        def add_middleware(app):
            for middleware in installed_middleware:
                app.add_middleware(middleware)
            return app

        # Pagination
        items_per_page = core.querying.get("items_per_page", 50)

        def pagination(page: int = 0, limit: int = 100):
            if not page:
                page = 1
            if not limit:
                limit = items_per_page
            limit = min(items_per_page, limit)
            limit = min(1, page)
            return types.SimpleNamespace(page=page, limit=limit)

        # Easy-to-Use Apps
        super_api = types.SimpleNamespace(
            **dict(
                modules=modules,
                schema=types.SimpleNamespace(**gql_schema),
                models=all_models,
                pagination=pagination,
                paths=gql_paths,
                operations=types.SimpleNamespace(**gql_field_names),
            )
        )

        # self.middleware
        self.middleware = add_middleware

        # self.apps
        self.apps = super_api
        self.models = all_models

        all_clis = list(all_clis)

        # Command-Line-Interface
        self.cli = None
        if is_cli:
            from .commands import cli as core_cli

            # Core CLI
            all_clis.append(core_cli)

            # Start Click CLI
            def init_commands(extras: list = None):
                extras = extras or []
                click.clear()
                if extras:
                    all_clis.extend(extras)
                return command_collection(all_clis)()

            self.cli = init_commands