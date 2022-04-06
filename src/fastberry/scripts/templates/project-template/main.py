# Framework
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# API (Schema)
from fastberry import Schema
from strawberry.fastapi import GraphQLRouter

# Settings
from config import settings

# Apps
APPS = settings.apps

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.base.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# All Routers
app.include_router(settings.router)

# GraphQL (Schema)
schema = Schema(
    query=APPS.schema.Query,
    mutation=APPS.schema.Mutation,
    extensions=[],
    introspection=(not settings.mode == "production"),
)

# GraphQL (Router)
app.include_router(
    GraphQLRouter(
        schema,
        graphiql=(not settings.mode == "production"),
    ),
    prefix="/graphql",
    tags=["GraphQL"],
)
