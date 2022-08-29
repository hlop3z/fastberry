""" Fastberry Core

    import pathlib

    # Build paths inside the project like this: BASE_DIR / "subdir".
    BASE_DIR = pathlib.Path(__file__).resolve().parents[1]

    # Or like this: settings.base_dir / "subdir".
    settings = Settings(base_dir=BASE_DIR)

classes:
    Settings: Singleton.
"""


import functools
import os
import pathlib
import sys
from types import SimpleNamespace

import click
import dbcontroller as dbc
from fastapi.routing import APIRouter

from ..utils.objects import Singleton
from .definitions import load_docs, load_env, load_mode, load_yaml
from .extras.click import command_collection
from .tools import (
    Database,
    default_databases,
    get_project_databases_settings,
    load_all_modules,
)


def not_found(base):
    """No Type Found"""
    return base


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
        core_settings_yaml = load_yaml()
        env_mode = load_mode().get("mode", "development")
        env = load_env(env_mode)

        # Keys
        self.keys = [
            "apps",
            "base",
            "base_dir",
            "cli",
            "debug",
            "docs",
            "env",
            "extensions",
            "middleware",
            "mode",
            "router",
            "secret_key",
            "project",
            # "pagination",
        ]

        # BASE_DIR
        self.base_dir = base_dir

        # Setup
        self.base = core_settings_yaml
        self.env = env
        self.docs = load_docs()
        self.mode = env_mode
        self.debug = env.debug
        self.secret_key = env.secret_key
        self.models = None

        # Model (DBC)
        fake_model_db = dbc.Model()
        self.type = fake_model_db.type

        # Router
        router = APIRouter()
        self.router = router

        # User Settings
        self.project = None
        self.controller = None  # Module: { DBController }
        self.database = None
        self.sql = not_found
        self.mongo = not_found
        self.cli = None  # Command-Line-Interface
        self.types = None
        self.apps = None
        self.middleware = None
        self.extensions = None
        self.on_event = None

        # Include BASE_DIR / "apps"
        if base_dir:
            sys.path.insert(0, os.path.join(base_dir, "apps"))
            # sys.path.insert(0, os.path.join(base_dir))

            try:
                import project

                self.project = project
            except ImportError:
                project = False

        # Project Configurations
        fake_model_db = SimpleNamespace(model=fake_model_db.type, admin=not_found)
        database_controller = Database(sql=fake_model_db, mongo=fake_model_db)
        self.database = database_controller
        if project:
            project_config = get_project_databases_settings(project)
            project_controller = project_config.get("databases")
            if project_controller:
                sql_default = project_controller.sql.get("default")
                mongo_default = project_controller.mongo.get("default")
                if sql_default or mongo_default:
                    database_controller = Database(
                        sql=sql_default,
                        mongo=mongo_default,
                    )

            # SELF - Definitions
            self.controller = project_controller  # Module: { DBController }
            self.database = database_controller
            if database_controller.sql:
                self.sql = database_controller.sql.model
            if database_controller.mongo:
                self.mongo = database_controller.mongo.model

        self.load_apps = functools.partial(
            self._step_2_handler,
            env_mode=env_mode,
            core_settings_yaml=core_settings_yaml,
            is_cli=is_cli,
        )

    def _step_2_handler(self, env_mode=None, core_settings_yaml=None, is_cli=None):
        """Real Loader"""
        api_manager = load_all_modules(
            env_mode=env_mode, core=core_settings_yaml, is_cli=is_cli
        )

        # SELF - Definitions
        API_TYPES = api_manager.types
        self.cli = None  # Command-Line-Interface
        self.types = API_TYPES
        self.apps = api_manager
        self.middleware = api_manager.add_middleware
        self.extensions = api_manager.graphql_extensions
        self.on_event = api_manager.events_extensions.__dict__

        # API - Models
        self.models = default_databases(self, API_TYPES)

        # CLI - Manager & Initializer
        if is_cli:
            from .commands import cli as core_cli

            # Core CLI
            api_manager.all_clis.append(core_cli)

            # Start Click CLI
            def init_commands(extras: list = None):
                extras = extras or []
                click.clear()
                if extras:
                    api_manager.all_clis.extend(extras)
                return command_collection(api_manager.all_clis)()

            self.cli = init_commands
