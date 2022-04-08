Settings are in **YAML** format. Because **YAML . . .**

> "is a human-readable data-serialization language". — **Wikipedia**

## **Settings** (YAML)

```yaml
# API INFORMATION
VERSION: 0.1.0
APP_NAME: Fastberry
ADMIN_EMAIL: fastberry@example.com

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

# [starlette-middleware](https://strawberry.rocks/docs/guides/custom-extensions)
EXTENSIONS:
  - myapp.extension.SomeExtension

# [strawberry-permissions](https://strawberry.rocks/docs/guides/permissions)
PERMISSIONS:
  - myapp.permissions.IsAuthorized

# GraphQL Output Folder
GENERATES: graphql
```

## **Breakdown** of the **Settings**

---

#### API INFORMATION

- **VERSION**: API's Current Version
- **APP_NAME**: API Name
- **ADMIN_EMAIL**: API's Admin Email

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

- **items_per_page**: Max number of items to grab from the database.
- **max_depth**: Max number for the depth of GraphQL queries.

---

#### MIDDLEWARE

---

#### EXTENSIONS

---

#### PERMISSIONS

---

#### GENERATES

---
