> Your code **needs** to be in a **file** named **`router.py`** inside your **Application**.

## File **Layout**

``` text
root/
|
|--  apps/
|    `--  MY_APP/               --> <Directory> - Your App is in HERE!
|        |-- __init__.py
|        `-- router.py          --> <File> - Your code goes in HERE!
|
`-- etc...
```

## Python **Code**

``` python title="router.py"
# -*- coding: utf-8 -*-
"""
    Router-Example
"""

from fastapi import APIRouter

router = APIRouter(
    tags=["Examples"],
)


@router.get("/hello_world")
async def hello_world():
    """Return: A `Hello World` Message."""

    return "Hello World"
```