# Demo-App (**Default** Setup)

> The **demo** application is created by **default** when you run the **`start-app`** command.

## CRUD

All methods inside **`Query`** and **`Mutation`** classes are by default **static**-methods **`@staticmethod`**

Each function is turn into a **`@staticmethod`** when it gets loaded after the server starts running.

That means you don't use **`self`** inside your functions.

### Command

```sh
./manage.py start-app my_app
```

### PyLint (**disable**)

> **E0213**: Method should have "**`self`**" as first argument (**no-self-argument**)

### Main **Five Operations**

> The demo-app comes with **`5`** core **`operations`**. (**Create, Update, Delete, Search** & **Detail**)

=== "GraphQL"

    | :material-pencil: Mutation     | :material-read: Query        |
    | ------------ | ------------ |
    | **`Create`** | **`Search`** |
    | **`Update`** | **`Detail`** |
    | **`Delete`** |              |

=== "CRUD"

    | Method       | CRUD        | GraphQL     | Description                                         |
    | ------------ | ----------- | ----------- | --------------------------------------------------- |
    | **`Create`** | Create      | `Mutation`  | :material-pencil:    Create resource                |
    | **`Update`** | Update      | `Mutation`  | :material-pencil:    Update resource                |
    | **`Delete`** | Delete      | `Mutation`  | :material-close:     Delete resource                |
    | **`Search`** | Read        | `Query`     | :material-read:      Fetch **Multiple** resources   |
    | **`Detail`** | Read        | `Query`     | :material-read:      Fetch **Single** resource      |

---

## App Layout

```text
my-app/                 --> <Directory> - Your App Root Directory.
|
|--  crud/              --> <Directory> - Your API's CRUD(s) Code in HERE.
|    |-- __init__.py    --> <File> - Import All Your CRUD Models in HERE.
|    `-- demo.py        --> <File> - CRUD Model Demo.
|
|--  operations/        --> <Directory> - Your GraphQL's Operations in HERE.
|    |-- core/          --> <File> - Used in both (Desktop & Mobile).
|    |-- desktop/       --> <File> - Used in Desktop.
|    `-- mobile/        --> <File> - Used in Mobile.
|
|-- __init__.py
|-- inputs.py           --> <File> - GraphQL Inputs.
|-- models.py           --> <File> - Database(s) Models.
`-- types.py            --> <File> - GraphQL Types.
```

---

### Variables (**optional**)

- **`schema`**: Requires a **(type) &lt;`strawberry.type`&gt;**.
- **`prefix`**: A prefix(**str**) to use **`before`** the function name.

### Classes

- **`Query`**: GraphQL "**Query**" functions.
- **`Mutation`**: GraphQL "**Mutation**" functions.

## Demo **Files**

=== "demo.py"

    ```python
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    # Fastberry
    from fastberry import CRUD


    # Create your API (GraphQL) here.
    class Demo(CRUD):
        """Demo Api"""

        schema = None
        prefix = "demo"

        class Query:
            """Query"""

            async def search(info) -> str:
                """Read the Docs"""
                print(info)
                return "Search"

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

            async def update(info) -> str:
                """Read the Docs"""
                print(info)
                return "Update"

            async def delete(info) -> str:
                """Read the Docs"""
                print(info)
                return "Delete"
    ```

=== "\_\_init\_\_.py"

    ```python
    # -*- coding: utf-8 -*-
    """
        CRUD - Init
    """

    from .demo import Demo
    ```
