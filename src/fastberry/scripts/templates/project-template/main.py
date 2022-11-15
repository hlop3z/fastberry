# -*- coding: utf-8 -*-
""" [Main]
    FastAPI's Main File.
"""

# FastAPI & Strawberry
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastberry.app import Controller
from strawberry.fastapi import GraphQLRouter

# FastAPI
app = Controller.context.app

# Global Variables
SPOC_ALLOWED_HOSTS = Controller.toml.get("api", {}).get("allowed_hosts")
SPOC_MAX_DEPTH = Controller.toml.get("api", {}).get("max_depth", 3)
SPOC_GRAPHQL_PATH = Controller.toml.get("api", {}).get("graphql_path", "graphql")

# (SPOC_GRAPHQL_PATH) Global Variables
if SPOC_GRAPHQL_PATH.startswith("/"):
    SPOC_GRAPHQL_PATH = SPOC_GRAPHQL_PATH[1:]

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
if Controller.extras and Controller.extras.middleware:
    Controller.extras.middleware(app)

# CORS
if SPOC_ALLOWED_HOSTS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SPOC_ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ALL Routers
if Controller.router:
    app.include_router(*Controller.router)

# GraphQL (Config)
if Controller.graphql:
    schema = Controller.graphql.schema(
        introspection=(not Controller.context.is_production),
        max_depth=SPOC_MAX_DEPTH,
        extensions=Controller.extras.extensions,
    )

    # GraphQL (Schema)
    if schema:
        app.include_router(
            GraphQLRouter(
                schema,
                graphiql=(not Controller.context.is_production),
            ),
            prefix=f"/{SPOC_GRAPHQL_PATH}",
            tags=["GraphQL"],
        )

# Startup
@app.on_event("startup")
async def startup_event():
    """Startup Methods"""
    if Controller.extras and Controller.extras.on_startup:
        for func in Controller.extras.on_startup:
            if func:
                func(Controller.context)


# Shutdown
@app.on_event("shutdown")
def shutdown_event():
    """Shutdown Methods"""
    if Controller.extras and Controller.extras.on_shutdown:
        for func in Controller.extras.on_shutdown:
            if func:
                func(Controller.context)
