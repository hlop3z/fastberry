# **Extension** Example

> Inject { **on_startup** } and { **on_shutdown** } Server Events.

## Creating an **`on-event`** method

!!! abstract "Context"

    - **`app`** = **FastAPI** object.
    - **`settings`** = **Settings** module.
    - **`controller`** = **Fastberry** object.

```python title="on_event.py"
def on_startup(context):
    print("Server Startup")
    print(context.app)
    print(context.settings)
    print(context.controller)

def on_shutdown(context):
    print("Server Shutdown")
```

## **Example** of built-in **`on-event`**

> **`fastberry.extras.redirect_root`** is a built-in **`on-event`** method.
> You can redirect the root-path **`http://localhost:8000/`** to **`http://localhost:8000/docs`**

```python title="on_event.py"
from fastapi.responses import RedirectResponse

def redirect_root(context):
    """Redirect"""

    @context.app.get("/", response_class=RedirectResponse)
    async def redirect_root():
        """Redirect To Docs"""
        return "/docs"

    return context
```

!!! info "Note"

    In the file **`spoc.toml`** inside your **`config`** folder.
    Add the **`on-event`** method.

```python title="config/spoc.toml"
[spoc]

# etc ...

[spoc.extra]
# etc ...
on_startup = ["fastberry.extras.redirect_root"]
on_shutdown = []
```
