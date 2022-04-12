# **Middleware** Example

> Get { **Authorization** } from the { **Cookies** } and inject it to the { **Headers** }.

## **Import** your Basics

```python
"""[Middleware]

Get { Authorization } from the { Cookies } and inject it to the { Headers }.
"""

from fastberry import BaseMiddleware

```

## Get **Authorization** Cookie

```python
class AuthenticatedCookieMiddleware(BaseMiddleware):
    """Get Authorization From Cookie"""

    async def dispatch(self, request, call_next):
        """Process Request and Inject Header"""
        if (
            "Authorization" not in request.headers
            and "Authorization" in request.cookies
        ):
            access_token = request.cookies.get("Authorization")
            request.headers.__dict__["_list"].append(
                (
                    "authorization".encode(),
                    f"Bearer {access_token}".encode(),
                )
            )
        response = await call_next(request)
        return response
```
