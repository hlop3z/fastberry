> Your code **needs** to be in a **file** named **`router.py`** inside your **Application**.

## File **Layout**

```text
root/
|
|--  apps/
|    `--  MY_APP/               --> <Directory> - Your App in HERE!
|        `-- router.py          --> <File> - Your code in HERE!
|
`-- etc...
```

## Python **Code**

```python title="router.py"
# -*- coding: utf-8 -*-
"""
    Router-Example
"""

from fastberry import Router

router = Router(
    tags=["Examples"],
)


# Create <Routers> here.
@router.get("/hello_world")
async def hello_world():
    """Return: A `Hello World` Message."""

    return "Hello World"
```
