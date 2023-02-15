"""
    On Events (FastAPI)
"""
from fastapi.responses import RedirectResponse


def redirect_root(context):
    """Redirect"""

    @context.app.get("/", response_class=RedirectResponse)
    async def redirect_to_docs():
        """Redirect To Docs"""
        return "/docs"

    return context
