# First **App**

```sh
pdm run startproject
```

<div id="terminal-getting-started-first-app" data-termynal></div>

## Settings `config/settings.py` (**Demo**)

```python title="config/settings.py"
# -*- coding: utf-8 -*-
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = ["demo"] # (1)
```

1. **INSTALLED_APPS** - Right now we control the **`INSTALLED_APPS`** from here. **However**, depending on **`mode`** in the **`spoc.toml`** is where you place them.
