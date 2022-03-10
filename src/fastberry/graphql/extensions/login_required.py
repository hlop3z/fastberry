import dataclasses
from types import SimpleNamespace

import strawberry
from graphql import GraphQLError
from strawberry.extensions import Extension
from strawberry.types import Info

from routers.users import decode_token, get_user


@dataclasses.dataclass
class Method:
    name: str = None
    field: str = None
    action: str = "read"


def get_token_bearer(info):
    token_bearer = info.context["request"].headers.get("AUTHORIZATION")
    token = None
    if token_bearer:
        token = token_bearer.replace("Bearer ", "", 1)
    return token


async def get_token(context):
    token = get_token_bearer(context)
    user = None
    if token:
        user_token = await decode_token(token)
        username = user_token.get("username")
        if username:
            user = get_user(username)
    return user


def find_field_type(info):
    output = None
    name = info.parent_type.name
    if name == "Mutation":
        output = Method(action="write", name=info.field_name)
    elif (
        name
        not in [
            "Query",
            "PageInfo",
        ]
        and not name.endswith("Edge")
        and not name.endswith("Connection")
    ):
        output = Method(action="read", name=name.lower(), field=info.field_name)
    return output


AUTHORIZED_EXCEPTION = GraphQLError("You Are Not Authorized.")


class LoginRequired(Extension):
    async def on_executing_start(self):
        user = await get_token(self.execution_context)
        self.execution_context.context["user"] = user
        if not user:
            self.execution_context.result = SimpleNamespace(
                data=None,
                errors=[AUTHORIZED_EXCEPTION],
            )
