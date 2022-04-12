Settings are in **YAML** format. Because **YAML . . .** is easy to read.

> "is a human-readable data-serialization language". — **Wikipedia**

## **Settings** (YAML)

```yaml
# API INFORMATION
VERSION: 0.1.0
APP_NAME: Fastberry
ADMIN_EMAIL: fastberry@example.com

# GraphQL Output Folder
GENERATES: graphql

ALLOWED_HOSTS:
  # 8080 (Front-End)
  - http://localhost:8080
  - http://127.0.0.1:8080

INSTALLED_APPS:
  - my_awesome_app

DEVELOPMENT_APPS:
  - some_development_tool

QUERYING:
  items_per_page: 50
  max_depth: 4

# [starlette-middleware](https://www.starlette.io/middleware/)
MIDDLEWARE:
  - myapp.middleware.AuthenticatedCookieMiddleware

# [strawberry-extensions](https://strawberry.rocks/docs/guides/custom-extensions)
EXTENSIONS:
  - myapp.extension.SomeExtension

# [strawberry-permissions](https://strawberry.rocks/docs/guides/permissions)
PERMISSIONS:
  - myapp.permissions.IsAuthorized
```

## **Breakdown** of the **Settings**

---

#### API INFORMATION

- **VERSION**: API's Current Version
- **APP_NAME**: API Name
- **ADMIN_EMAIL**: API's Admin Email

---

#### GENERATES

> Output folder for **GraphQL Schema & Operations**.

---

#### ALLOWED_HOSTS

> List of **Allowed Hosts** that can connect to the server.

---

#### INSTALLED_APPS

> List of **Installed Apps** that are currently used in this project.

---

#### DEVELOPMENT_APPS

> List of **Development Apps** that are active when the server is running on **development mode**.

---

#### QUERYING

- **items_per_page**: Max number of items to grab from the **Database**.
- **max_depth**: Max number for the depth of **GraphQL Queries**.

---

#### MIDDLEWARE [(Starlette)](https://www.starlette.io/middleware/)

> List of active **Middlewares**.

You can create your own **middleware** by using the **base module**.

The **BaseMiddleware** included is just a wrapper/rename for **BaseHTTPMiddleware** from **Starlette**

---

#### EXTENSIONS [(Strawberry)](https://strawberry.rocks/docs/guides/custom-extensions)

> List of active **Extensions**.

You can create your own **extension** by using the **base module**.

The **BaseExtension** included is just a wrapper/rename for **Extension** from **Strawberry**

---

#### PERMISSIONS [(Strawberry)](https://strawberry.rocks/docs/guides/permissions)

> List of active **Permissions**.

You can create your own **permissions** by using the **base module**.

The **BasePermission** included is just a wrapper for **BasePermission** from **Strawberry**

---
