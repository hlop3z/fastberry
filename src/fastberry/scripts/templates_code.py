"""{ Global Values }
    Code for creating the core files in order to run the API.
"""

SETTINGS = '''
# -*- coding: utf-8 -*-
"""
    { Settings }
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = []

# Database(s)
DATABASES = {
    "sql": {"default": None},  # Example: sqlite:///example.db
    "mongo": {"default": None},  # Example: mongodb://localhost:27017/example
}
'''.strip()

SPOC = """
[spoc]
mode = "custom"
custom_mode = "development"
docs = "config/docs.md"
generates = "graphql"

[spoc.api]
graphql_path = "/graphql"
max_depth = 4
items_per_page = 50
allowed_hosts = ["http://localhost", "http://localhost:8080"]

[spoc.apps]
production = []
development = []
staging = []

[spoc.extras]
middleware = []
extensions = []
permissions = []
on_startup = ["fastberry.extras.redirect_root"] # "fastberry.extras.graphql_info"
on_shutdown = []
""".strip()


DOCS = """
# Welcome

> This is a simple **API** Skeleton

---

## Links

> Go To [GraphQL](/graphql)

---

## Mode (Options)

- `development`

- `staging`

- `production`

---

## Settings Layout

```text
root/                           --> <Directory> - Project's Root.
|
|--  config/                    --> <Directory> - Configurations.
|    |
|    |-- .env/                  --> <Directory> - Environments.
|    |   |
|    |   |-- development.toml   --> <File> - Development    | Settings.
|    |   |-- production.toml    --> <File> - Production     | Settings.
|    |   `-- staging.toml       --> <File> - Staging        | Settings.
|    |
|    |-- docs.md                --> <File> - This Documentation is in HERE.
|    |-- settings.py            --> <File> - Python         | Settings.
|    `-- spoc.toml              --> <File> - TOML           | Settings.
|
|-- pyproject.toml              --> <File> - Project        | Settings.
|
`-- etc...
```
""".strip()
