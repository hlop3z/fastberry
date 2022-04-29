# -*- coding: utf-8 -*-
""" [Main]
    FastAPI Main File.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from strawberry.fastapi import GraphQLRouter

# API (Config)
from config import settings

# API (Schema)
from fastberry import Schema

# FastAPI
app = FastAPI(
    description=settings.docs,
    title=settings.base.app_name,
    version=settings.base.version,
)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
settings.middleware(app)

# CORS
if settings.base.allowed_hosts:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.base.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ALL Routers
app.include_router(settings.router)

# GraphQL (Schema)
schema = Schema(
    query=settings.apps.schema.Query,
    mutation=settings.apps.schema.Mutation,
    extensions=[],
    introspection=(not settings.mode == "production"),
)

# GraphQL (Router)
if schema:
    app.include_router(
        GraphQLRouter(
            schema,
            graphiql=(not settings.mode == "production"),
        ),
        prefix="/graphql",
        tags=["GraphQL"],
    )

# Startup
@app.on_event("startup")
async def startup_event():
    for func in settings.on_event["startup"]:
        func()


# Shutdown
@app.on_event("shutdown")
def shutdown_event():
    for func in settings.on_event["shutdown"]:
        func()


# Redirect To Docs
@app.get("/", response_class=RedirectResponse)
async def redirect_fastapi():
    return "/docs"
