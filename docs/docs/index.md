# Welcome to **Fastberry**

Fastberry, is built with **FastAPI** and **Strawberry** that is why it was called **Fastberry**.

**Click** is used to manage the server and development process.

**dbcontroller** is used to manage the requests to the databases (SQL or Mongo).

**Uvicorn** is used to run the server in **development** and **staging** mode.

**Gunicorn** is used to run the server in **production** mode.

### Built With:

- [Click](https://github.com/pallets/click/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Strawberry](https://strawberry.rocks/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Database-Controller](https://hlop3z.github.io/dbcontroller/)
- [Uvicorn](https://www.uvicorn.org/)
- [Gunicorn](https://gunicorn.org/)

---

## **Core** Layout

```text
root/                           --> <Directory> - Project's Root.
|
|--  apps/                      --> <Directory> - Modules (aka: Apps) in HERE.
|
|--  config/                    --> <Directory> - Configurations.
|    |-- __init__.py            --> <File> - Load Settings.
|    |-- docs.md                --> <File> - API's Documentation in HERE.
|    |
|    |-- env/                   --> <Directory> - Environments.
|    |   |-- development.env    --> <File> - Development.
|    |   |-- production.env     --> <File> - Production.
|    |   `-- staging.env        --> <File> - Staging.
|    |
|    `-- mode.json              --> <File> - Current Mode.
|
|-- main.py                     --> <File> - FastAPI main.py file.
|-- manage.py                   --> <File> - Run (CLI) Command-Line-Interface.
|-- settings.yaml               --> <File> - Base Settings.
`-- etc...
```

---

## Inspired By **Django**

There are several things from Django that inspire this tool.

Some of the commands and the installation of **modules** (aka: **INSTALLED_APPS**) inside a Django project.

### **Fastberry** comes with a few key **commands**:

- **`./manage.py run`** Start **FastApi Server**
- **`./manage.py schema`** Build **GraphQL (Schema + Operations)**
- **`./manage.py start-app`** Create a **Fastberry App** Directory inside your "**`apps`**" directory.

## **Mode** (Options)

> **`./manage.py run`** Start **FastApi Server**

- `development`

- `staging`

- `production`

> **`./manage.py run --help`** For **more information**.

---

## **Settings** (YAML)

```yaml
# API Information
VERSION: 0.1.0
APP_NAME: Fastberry
ADMIN_EMAIL: fastberry@example.com

# Installed Apps
INSTALLED_APPS:
  - my_awesome_app

# Development Apps
DEVELOPMENT_APPS:
  - some_development_tool

# Querying
QUERYING:
  items_per_page: 50

# Allowed Hosts
ALLOWED_HOSTS:
  # 8080 (Front-End)
  - http://localhost:8080
  - http://127.0.0.1:8080
```
