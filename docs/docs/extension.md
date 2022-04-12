# **Extension** Example

> Inject { **User** } or { **Anonymous-User** } to **GraphQL Context**.

## **Import** your Basics

```python
"""[Extension]

Inject { User } or { Anonymous-User } to GraphQL Context.
"""

import secrets

from pydantic import BaseModel

from fastberry import BaseExtension

```

## Create the **User class** with **pydantic** or **dataclasses**

```python
class User(BaseModel):
    """API User"""

    id: str
    role: str
    username: str
    email: str
    full_name: str | None = None
    disabled: bool = False
    is_staff: bool = False
    super_user: bool = False
    is_authenticated: bool = False
    is_anonymous: bool = False

```

## **Anonymous**-User or **Authenticated**-User?

```python
def anonymous_user():
    """Default Anonymous User"""
    token = f"anonymous-{secrets.token_urlsafe(38)}"
    user = User(
        id=token,
        role="public",
        username="fastberry",
        email="fake@example.com",
        is_anonymous=True,
    )
    return user


async def get_request_user(request):
    """Get User from Request the Header or Cookie"""
    print(request)
    return None
```

## Create your Strawberry / Fastberry **Extension**

```python
class LoginRequired(BaseExtension):
    """Login Required Extension"""

    async def on_executing_start(self):
        request = self.execution_context.context.get("request")
        user = await get_request_user(request)

        if not user:
            # Anonymous-User
            user = anonymous_user()
        else:
            # User-Authenticated
            user = User(**user.__dict__, is_authenticated=True)

        # Set-User (Context)
        self.execution_context.context["user"] = user
```
