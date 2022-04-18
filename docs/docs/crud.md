> Your code **needs** to be in a **file** named **`crud.py`** or **folder** named **`crud`** inside your **Application**.

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- crud.py            --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- crud/               --> <Directory> - Your CRUD in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

## Python **Code**

=== ":material-file: File"

    ``` python title="crud.py"
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    # Fastberry
    from fastberry import CRUD


    # Create your API (GraphQL) here.
    class Demo(CRUD):
        """Demo Api"""

        class Query:
            """Query"""

            async def detail(info) -> str:
                """Read the Docs"""
                print(info)
                return "Detail"

        class Mutation:
            """Mutation"""

            async def create(info) -> str:
                """Read the Docs"""
                print(info)
                return "Create"
    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
        CRUD - Init
    """

    # Import your <cruds> here.
    from .demo import Demo
    ```

    ``` python title="demo.py"
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    # Fastberry
    from fastberry import CRUD


    # Create your API (GraphQL) here.
    class Demo(CRUD):
        """Demo Api"""

        class Query:
            """Query"""

            async def detail(info) -> str:
                """Read the Docs"""
                print(info)
                return "Detail"

        class Mutation:
            """Mutation"""

            async def create(info) -> str:
                """Read the Docs"""
                print(info)
                return "Create"
    ```
