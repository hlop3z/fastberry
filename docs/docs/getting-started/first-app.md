# First **App**

```sh
pdm app start-app demo
```

<div id="terminal-getting-started-first-app" data-termynal></div>

## Settings `config/settings.py` (**Demo**)

!!! note "Installed Apps"

    After creating your first **`demo`** app. Install it in the applications list "**`INSTALLED_APPS`**"

```python title="config/settings.py"
# -*- coding: utf-8 -*-
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = ["demo"] # (1)
```

1. **INSTALLED_APPS** - Right now we control the **`INSTALLED_APPS`** from here. **However**, depending on **`mode`** in the **`spoc.toml`** is where you place them.

!!! note "Run"

    Start the Server (Again). After adding your **App** to **`INSTALLED_APPS`**.

    ```sh
    pdm app run
    ```

    Then go to <a href="http://127.0.0.1:8000/graphql" target="_blank">**http://127.0.0.1:8000/graphql**</a>

!!! tip "GraphQL"

    If its working it should look something like the **image below**.

![GraphQL](img/graphql.png)
