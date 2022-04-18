# **Plugin** Example

> Coming full circle with all **Four-Elements** (Middleware, Extension, Permissions and Router)

---

## Command

```sh
./manage.py start-app my_awesome_plugin --plugin
```

---

## File **Layout**

```text
root/
|
|--  apps/
|    `--  MY_PLUGIN/             --> <Directory> - Your App in HERE!
|        |-- extension.py
|        |-- middleware.py
|        |-- permission.py
|        |-- router.py
|        `-- users.py
|
`-- etc...
```

---

## Other **Requirements**

```sh
python -m pip install "python-jose[cryptography]" "passlib[bcrypt]"
```

---

## Demo **Credentials**

- **Username**: **`johndoe`** or **`janedoe`**
- **Password**: **`secret`**

---

=== "users.py"

    ```python title="users.py"
    # -*- coding: utf-8 -*-
    """
        [Users]
    """

    from datetime import datetime, timedelta
    from typing import Optional

    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer
    from jose import JWTError, jwt
    from passlib.context import CryptContext
    from pydantic import BaseModel

    SECRET_KEY = "fastapi-insecure-09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b"

    # Security
    ALGORITHM = "HS256"

    FAKE_USERS_DB = {
        "johndoe": {
            "id": 1,
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
            "is_staff": True,
            "super_user": False,
        },
        "janedoe": {
            "id": 2,
            "username": "janedoe",
            "full_name": "Jane Doe",
            "email": "janedoe@example.com",
            "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
            "disabled": False,
            "is_staff": False,
            "super_user": False,
        },
    }

    FAKE_ROLES_DB = {1: "admin", 2: "public"}


    class UserLogin(BaseModel):
        username: str
        password: str


    class Token(BaseModel):
        access_token: str
        token_type: str


    class User(BaseModel):
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


    class UserInDB(User):
        hashed_password: str


    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(password):
        return pwd_context.hash(password)


    async def get_user(username: str):
        db = FAKE_USERS_DB
        role_db = FAKE_ROLES_DB
        if username in db:
            user_dict = db[username]
            role = role_db.get(user_dict.get("id"))
            user_dict["role"] = role
            return UserInDB(**user_dict)


    async def get_request_user(request):
        access_token = request.headers.get("Authorization")
        user = None
        if access_token:
            token = access_token.replace("Bearer ", "")
            auth_dict = await decode_token(token)
            if auth_dict:
                username = auth_dict.get("username")
                user = await get_user(username=username)
        return user


    async def authenticate_user(username: str, password: str):
        user = await get_user(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user


    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    async def decode_token(token: str):
        try:
            return_value = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return_value = {}
        return return_value


    async def get_current_user(
        token: Optional[str] = Depends(oauth2_scheme),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = await decode_token(token)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        user = await get_user(username=username)
        if user is None:
            raise credentials_exception
        return user


    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    ```

=== "router.py"

    ```python title="router.py"
    # -*- coding: utf-8 -*-
    """
        [Router]
    """

    from datetime import timedelta

    from fastapi import APIRouter, Depends, HTTPException, Response, status
    from fastapi.responses import JSONResponse
    from fastapi.security import OAuth2PasswordRequestForm

    from .users import (
        Token,
        User,
        authenticate_user,
        create_access_token,
        get_current_active_user,
    )

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

    router = APIRouter(
        tags=["Users"],
    )


    def to_camel_case(text):
        init, *temp = text.split("_")
        return "".join([init.lower(), *map(str.title, temp)])


    @router.post("/token", response_model=Token)
    async def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=access_token_expires,
        )
        response.set_cookie(
            key="Authorization", value=access_token, httponly=True, secure=True
        )
        return {"access_token": access_token, "token_type": "bearer"}


    @router.get("/logout")
    async def logout_user(current_user: User = Depends(get_current_active_user)):
        response = JSONResponse({"logout": True})
        response.delete_cookie(key="Authorization")
        return response


    @router.get("/user-me")  # response_model=User
    async def read_users_me(current_user: User = Depends(get_current_active_user)):
        user_me = {to_camel_case(k): v for k, v in current_user.__dict__.items()}
        del user_me["hashedPassword"]
        return user_me

    ```

=== "extension.py"

    ```python title="extension.py"
    # -*- coding: utf-8 -*-
    """ [Extension]
        Inject { User } or { Anonymous-User } to GraphQL Context.
    """

    import secrets

    from fastberry import BaseExtension

    from .user import User, get_request_user


    def anonymous_user():
        """Default Anonymous User"""

        token = f"anonymous-{secrets.token_urlsafe(38)}"
        user = User(
            id=token,
            role="public",
            is_anonymous=True,
        )
        return user


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
                user = User(**user.__dict__, is_authenticated=True)

            # Set-User (Context)
            self.execution_context.context["user"] = user
    ```

=== "middleware.py"

    ```python title="middleware.py"
    # -*- coding: utf-8 -*-
    """ [Middleware]
        Get { Authorization } from the { Cookies } and inject it to the { Headers }.
    """

    from fastberry import BaseMiddleware


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

=== "permission.py"

    ```python title="permission.py"
    # -*- coding: utf-8 -*-
    """ [Permission]
        Check GraphQL Context for a { User } or { Anonymous-User }.
    """

    import typing

    from strawberry.types import Info

    from fastberry import BasePermission

    ROLES = {"public": ["SomeMethod"]}


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
