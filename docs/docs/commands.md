> Your code **needs** to be in a **file** named **`commands.py`**  or **folder** named **`commands`** inside your **Application**.

## File or Folder **Layout**

=== "File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- commands.py          --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== "Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- commands/           --> <Directory> - Your Commands in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

## Python **Code**

``` python title="commands.py"
# -*- coding: utf-8 -*-
"""
    Project - Commands
"""
import click


@click.group()
def cli():
    pass


@cli.command()
def hello_world():
    """Demo CLI Function"""
    print("Hello World")
```
