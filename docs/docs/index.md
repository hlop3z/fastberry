# Welcome to **Fastberry**

Fastberry, is built with **FastAPI** and **Strawberry** that is why is named **Fastberry**.

The **`manager`** is built with **Click**.

### **Built** With:

| Module                                                       | Is Used To...                                                         |
| ------------------------------------------------------------ | --------------------------------------------------------------------- |
| [**Click**](https://github.com/pallets/click/)               | **Manage** the server, development process and custom **`Commands`**. |
| [**FastAPI**](https://fastapi.tiangolo.com/)                 | **Core** Web **`Framework`**                                          |
| [**Strawberry**](https://strawberry.rocks/)                  | **GraphQL** **`Library`**                                             |
| [**PyYAML**](https://pypi.org/project/PyYAML/)               | **Load** the project **`Settings`**.                                  |
| [**Python-Dotenv**](https://pypi.org/project/python-dotenv/) | **Load** the **`Environment Variables`**.                             |
| [**Pydantic**](https://pydantic-docs.helpmanual.io/)         | **Format** `Environment Variables` and more **FastAPI** uses.         |
| [**Uvicorn**](https://www.uvicorn.org/)                      | **Run** the server in **`Development`** mode.                         |
| [**Gunicorn**](https://gunicorn.org/)                        | **Run** the server in **`Staging`** and **`Production`** mode.        |

---

## **Install** Fastberry

```sh
python -m pip install fastberry
```

## **Install** Uvicorn + Gunicorn

```sh
python -m pip install "uvicorn[standard]" gunicorn
```

---

## **Module** Workflow

> You can create **`commands`** or **`fastapi`** and **`strawberry-graphql`** endpoints.

```mermaid
graph LR;
    A{Click} --> B[Uvicorn];
    A --> C[Gunicorn];
    A --- D[Load Settings & APIs];
    B --> E{FastAPI};
    C --> E;
    E --- F[Load Settings & APIs];
    D --- |Strawberry-GraphQL| G{Your Commands};
    F --- |Strawberry-GraphQL| H{Your API};
    H --> Z{Your Code};
    G --> Z;
```

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
|    |   |-- development.env    --> <File> - Development Settings.
|    |   |-- production.env     --> <File> - Production Settings.
|    |   `-- staging.env        --> <File> - Staging Settings.
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

- **`startproject`** Create a new **Fastberry** project.
- **`./manage.py run`** Run **FastApi Server**.
- **`./manage.py schema`** Build **GraphQL (Schema + Operations)**.
- **`./manage.py start-app`** Create a **Fastberry App** inside your "**`apps`**" directory.
- **`./manage.py --help`** For **more information**.

## **Mode** (Options)

> **`./manage.py run`** Start **FastApi Server**

- `development`

- `staging`

- `production`

> **`./manage.py run --help`** For **more information**.
