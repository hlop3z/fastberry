# First **Type**

!!! warning

    For the example **first** setup a **SQLite** database in the settings file.

## Settings

```python title="config/settings.py"
# -*- coding: utf-8 -*-
"""
    { Settings }
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = ["demo"]

# Database(s)
DATABASES = {
    "sql"  : {"default": "sqlite:///example.db"},
    "mongo": {"default": None},
}
```

## Type

!!! info

    Creating **`Book`** as our first **`Type`**

```python title="apps/demo/types.py"
# -*- coding: utf-8 -*-
"""
    { Types } for GraphQL
"""

from typing import Optional
import fastberry as fb

# Create your <types> here.
@fb.sql.model
class Book:
    """(Type) Read The Docs"""

    title: str
    author: str
```

## Database Migrations

```sh
pdm app db auto-migrate
```

!!! warning

    Keep in mind that migrations are only for **`SQL`**

<div id="terminal-getting-started-first-type" data-termynal></div>

!!! note "Run"

    **Then**, Start the Server (Again).

    ```sh
    pdm app run
    ```
