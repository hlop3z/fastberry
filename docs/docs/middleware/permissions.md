# **Permission** Example

> Check **GraphQL Context** for a { **User** } or { **Anonymous-User** }.

=== "Tutorial"

    ## **Import** your Basics

    ```python
    # -*- coding: utf-8 -*-
    """ [Permission]
        Check GraphQL Context for a { User } or { Anonymous-User }.
    """

    import typing

    from strawberry.types import Info

    from fastberry import BasePermission

    ```

    ## Get User **Permissions**

    ```python
    ROLES = {
        "public": ["SomeMethod"],
        "admin": ["demoDetail", "demoSearch", "demoCreate", "demoUpdate", "demoDelete"],
    }

    def get_perms(role: str = None):
        """Get Role And Check For Permissions"""

        found = ROLES.get(role, [])
        if found and role:
            perms = found
        else:
            perms = []
        return perms

    ```

    ## Create your Strawberry / Fastberry **Permission**

    For more information about **custom permissions** go to [**strawberry**: custom-permissions](https://strawberry.rocks/docs/guides/permissions)

    ```python
    class IsAuthorized(BasePermission):
        """Check If User Is Authorized"""

        message = "User is not authorized"  # Unauthorized

        async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
            """Check GraphQL's Info Context"""

            # if not user.is_authenticated and user.is_anonymous:
            operation = info.field_name  # info.python_name
            user = info.context.get("user")
            if user:
                permissions = get_perms(user.role)
                return operation in permissions
            return False
    ```

=== "Full-Code"

    ``` python title="permissions.py"
    # -*- coding: utf-8 -*-
    """ [Permission]
        Check GraphQL Context for a { User } or { Anonymous-User }.
    """

    import typing

    from strawberry.types import Info

    from fastberry import BasePermission

    ROLES = {
        "public": ["SomeMethod"],
        "admin": ["demoDetail", "demoSearch", "demoCreate", "demoUpdate", "demoDelete"],
    }


    def get_perms(role: str = None):
        """Get Role And Check For Permissions"""

        found = ROLES.get(role, [])
        if found and role:
            perms = found
        else:
            perms = []
        return perms


    class IsAuthorized(BasePermission):
        """Check If User Is Authorized"""

        message = "User is not authorized"  # Unauthorized

        async def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
            """Check GraphQL's Info Context"""

            # if not user.is_authenticated and user.is_anonymous:
            operation = info.field_name  # info.python_name
            user = info.context.get("user")
            if user:
                permissions = get_perms(user.role)
                return operation in permissions
            return False
    ```
