# Welcome to **Fastberry**

Fastberry, is built with **FastAPI** and **Strawberry** that is why is named **Fastberry**.

The **`Command-Line-Interface` (CLI)** is built with **Click**.

<div id="terminal-index" data-termynal></div>

---

## **Description**

A tool for building **`GraphQL — API(s)`** with **`Python`**.

!!! info "You can create . . ."

    1. **`GraphQL`** — **`Query`**(s) and **`Mutation`**(s).
    2. **`API`** — HTTP **`Operation`**(s).
    3. **`Commands`** — To create automated processes and more . . .

---

## **Built** With

| Module                                                                                | Is Used To...                                                         |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| <a href="https://github.com/pallets/click/" target="_blank">**Click**</a>             | **Manage** the server, development process and custom **`Commands`**. |
| <a href="https://fastapi.tiangolo.com/" target="_blank">**FastAPI**</a>               | **Core** Web **`Framework`**                                          |
| <a href="https://strawberry.rocks/" target="_blank">**Strawberry**</a>                | **GraphQL** **`Library`**                                             |
| <a href="https://www.uvicorn.org/" target="_blank">**Uvicorn**</a>                    | **Run** the server in **`Development`** mode.                         |
| <a href="https://gunicorn.org/" target="_blank">**Gunicorn**</a>                      | **Run** the server in **`Staging`** and **`Production`** mode.        |
| <a href="https://pypi.org/project/spoc/" target="_blank">**SPOC**</a>                 | **FrameWork** tool for building this **`Framework`**.                 |
| <a href="https://pypi.org/project/dbcontroller/" target="_blank">**DBController**</a> | **Database** Controller for **`SQL`** and **`Mongo`**.                |

---

## Install **Fastberry** (Demo)

```sh
python -m pip install "fastberry[testing]"
```

## Install Fastberry **Mongo**

```sh
python -m pip install "fastberry[mongo]"
```

## Install Fastberry **SQL**

```sh
python -m pip install "fastberry[sql]" "databases[sqlite]"
```

!!! info "SQL Options"

    | Database   | Extra Installation(s)         |
    | ---------- | ----------------------------- |
    | PostgreSQL | **`"databases[postgresql]"`** |
    | MySQL      | **`"databases[mysql]"`**      |
    | Sqlite     | **`"databases[sqlite]"`**     |

## **Install** Gunicorn

```sh
python -m pip install gunicorn
```

---

## Project **Flowchart**

!!! info "You can create . . ."

    **`Command(s)`** | **`API(s)`** | **`GraphQL`** <span class="cool-text">**Components**</span>.

| <span class="cool-text">**(API)**</span> Application Programming Interface | <span class="cool-text">**(CLI)**</span> Command-Line Interface    |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 1. Load all **`Settings`**.                                                | 1. Load all **`Settings`**.                                        |
| 2. Load **`Environment Variables`**.                                       | 2. Load **`Environment Variables`**.                               |
| 3. Load all **`Apps (Modules)`**.                                          | 3. Load all **`Apps (Modules)`**.                                  |
| 4. Start the **`API`** <span class="cool-text">**Server**</span>.          | 4. Start the **`CLI`** <span class="cool-text">**Manager**</span>. |

```mermaid
flowchart LR;
    A{Click} --> B[Uvicorn];
    A --> C[Gunicorn];
    A <--> D[Load Settings & Modules];
    B --> E{FastAPI};
    C --> E;
    E <--> F[Load Settings & Modules];
    D <--> |Strawberry-GraphQL| G{Your Commands};
    F <--> |Strawberry-GraphQL| H{Your API};
    H <--> Z{Your Code};
    G <--> Z;
```

---

## **Core** Layout

```text
root/                           --> <Directory> - Project's Root.
|
|-- apps/                       --> <Directory> - Project's Apps.
|
|--  config/                    --> <Directory> - Configurations.
|    |
|    |-- .env/                  --> <Directory> - Environments.
|    |   |-- development.env    --> <File> - Development    | Settings.
|    |   |-- production.env     --> <File> - Production     | Settings.
|    |   `-- staging.env        --> <File> - Staging        | Settings.
|    |
|    |-- docs.md                --> <File> - API's Documentation in HERE.
|    |-- settings.py            --> <File> - API (Pythonic) | Settings.
|    `-- spoc.toml              --> <File> - API (TOML)     | Settings.
|
|-- pyproject.toml              --> <File> - Project (TOML) | Settings.
|
`-- etc...
```

---

## Inspired By **Django**

There are several things from Django that inspire this tool.

Some of the commands and the installation of **modules** (aka: **INSTALLED_APPS**) inside a Django project.

### **Fastberry** comes with a few key **commands**:

| Command                     | Is Used To...                                                  |
| --------------------------- | -------------------------------------------------------------- |
| **`startproject`**          | Create a new **Fastberry** project.                            |
| **`./manage.py run`**       | Run **FastApi Server**.                                        |
| **`./manage.py schema`**    | Build **GraphQL (Schema + Operations + ReturnTypes)**.         |
| **`./manage.py start-app`** | Create a **Fastberry App** inside your "**`apps`**" directory. |
| **`./manage.py --help`**    | For **more information**.                                      |

!!! warning "startproject"

    Careful with the command `startproject`. Only **use it once** and make sure you are in a **new folder**.
    It will write files and folders.
