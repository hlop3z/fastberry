"""
    On Events (FastAPI)
"""
from fastapi.responses import RedirectResponse

from ..handlers.cmd.action import introspection_info


def redirect_root(context):
    """Redirect"""

    @context.app.get("/", response_class=RedirectResponse)
    async def redirect_to_docs():
        """Redirect To Docs"""
        return "/docs"

    return context


def graphql_info(context):
    """Get Graphql INFO"""
    schema = context.controller.graphql.schema()

    @context.app.get("/graphql-info")
    async def get_graphql_info():
        """Get Graphql INFO"""
        return introspection_info(schema)

    return context
