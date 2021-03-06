# **Extension** Example

> Inject { **User** } or { **Anonymous-User** } to **GraphQL Context**.

---

#### EXTENSIONS [(Strawberry)](https://strawberry.rocks/docs/guides/custom-extensions)

You can create your own **extension** by using the **base module**.

The **BaseExtension** included is just a wrapper/rename for **Extension** from **Strawberry**

=== "Tutorial"

    ## **Import** your Basics

    ``` python
    # -*- coding: utf-8 -*-
    """ [Extension]
        Inject { User } or { Anonymous-User } to GraphQL Context.
    """

    import secrets

    from pydantic import BaseModel

    from fastberry import BaseExtension

    ```

    ## Create the **User class** with **pydantic** or **dataclasses**

    ``` python
    class User(BaseModel):
        """API User"""

        id: str
        role: str
        username: str | None = None
        email: str | None = None
        full_name: str | None = None
        disabled: bool = False
        is_staff: bool = False
        super_user: bool = False
        is_authenticated: bool = False
        is_anonymous: bool = False

    ```

    ## **Anonymous**-User or **Authenticated**-User?

    ``` python
    def anonymous_user():
        """Default Anonymous User"""

        token = f"anonymous-{secrets.token_urlsafe(38)}"
        user = User(
            id=token,
            role="public",
            is_anonymous=True,
        )
        return user


    async def get_request_user(request):
        """Get User from Request the Header or Cookie"""

        print(request)
        return None
    ```

    ## Create your Strawberry / Fastberry **Extension**

    For more information about **custom extensions** go to [**strawberry**: custom-extensions](https://strawberry.rocks/docs/guides/custom-extensions)

    ``` python
    class InjectUser(BaseExtension):
        """Inject User Extension"""

        async def on_executing_start(self):
            request = self.execution_context.context.get("request")
            user = await get_request_user(request)

            if not user:
                # Anonymous-User
                user = anonymous_user()
            else:
                # User-Authenticated
                user_dict = user.__dict__
                user_dict["is_authenticated"] = True
                user = User(**user_dict)

            # Set-User (Context)
            self.execution_context.context["user"] = user
    ```

=== "Full-Code"

    ``` python title="extension.py"
    # -*- coding: utf-8 -*-
    """ [Extension]
        Inject { User } or { Anonymous-User } to GraphQL Context.
    """

    import secrets

    from pydantic import BaseModel

    from fastberry import BaseExtension


    class User(BaseModel):
        """API User"""

        id: str
        role: str
        username: str | None = None
        email: str | None = None
        full_name: str | None = None
        disabled: bool = False
        is_staff: bool = False
        super_user: bool = False
        is_authenticated: bool = False
        is_anonymous: bool = False


    def anonymous_user():
        """Default Anonymous User"""

        token = f"anonymous-{secrets.token_urlsafe(38)}"
        user = User(
            id=token,
            role="public",
            is_anonymous=True,
        )
        return user


    async def get_request_user(request):
        """Get User from Request the Header or Cookie"""

        print(request)
        return None


    class InjectUser(BaseExtension):
        """Inject User Extension"""

        async def on_executing_start(self):
            request = self.execution_context.context.get("request")
            user = await get_request_user(request)

            if not user:
                # Anonymous-User
                user = anonymous_user()
            else:
                # User-Authenticated
                user_dict = user.__dict__
                user_dict["is_authenticated"] = True
                user = User(**user_dict)

            # Set-User (Context)
            self.execution_context.context["user"] = user
    ```
