"""
    Framework
"""
from types import SimpleNamespace

import spoc
from fastapi import FastAPI

from . import handlers

PLUGINS = ["types", "forms", "graphql", "router", "commands"]


def create_api(self):
    """FastAPI Builder"""

    hide_docs = dict()
    if self.context.is_production:
        hide_docs["docs_url"] = None
        hide_docs["redoc_url"] = None

    app = FastAPI(
        title=self.info.title.title(),
        version=self.info.version,
        description=self.info.description,
        **hide_docs
    )
    # App Context
    self.context.app = app
    self.context.controller = self


@spoc.singleton
class Fastberry:
    """Framework"""

    def init(
        self,
    ):
        """Class __init__ Replacement"""
        framework = spoc.App(plugins=PLUGINS)

        # Self { Definitions }
        core_toml = framework.config["spoc"].get("spoc", {})

        self.settings = framework.settings
        self.context = SimpleNamespace(
            settings=framework.settings,
            is_production=core_toml.get("mode", "development") == "production",
        )

        # Info
        self.info = handlers.api_info(
            base_dir=framework.base_dir,
            pyproject=framework.config["pyproject"],
            toml=framework.config["spoc"],
        )

        # Create API
        create_api(self)
        self.core = framework
        self.extras = None
        self.router = None
        self.graphql = None
        self.toml = core_toml

        # Pagination : print(self.pagination(page=0, limit=500))
        self.pagination = handlers.pagination(core_toml)

        # FastAPI { Extras }
        self.extras = handlers.extras(framework.extras.items())

        if framework.component:
            # FastAPI { Routers }
            self.router = handlers.routers(framework.component.router.values())

            # GraphQL { Types }
            self.types = handlers.types(framework.component.types.values())

            # GraphQL { Forms }
            self.forms = handlers.forms(framework.component.forms.values())

            # GraphQL { Query & Mutation }
            self.graphql = handlers.graphql(
                schemas=framework.component.graphql.values(),
                permissions=self.extras.permissions,
            )

            # Command-Line-Interface
            self.cli = handlers.commands(framework.component.commands.values())

    def keys(self):
        """Finally: Collect { Keys }"""
        return sorted(
            [
                x
                for x in dir(self)
                if not x.startswith("_") and x not in ["init", "keys"]
            ]
        )


def graphql_schema():
    """GraphQL Schema

    Methods:
        * execute
        * execute_sync

    Example:

        schema.execute("graphql-query", variable_values={"key": "value"})

    Returns:
        schema: GraphQL-Schema
    """
    app = Fastberry()
    return app.graphql.schema()
