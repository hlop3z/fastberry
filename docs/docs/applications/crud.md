# C.R.U.D Application (**Default** Setup)

!!! info

    The **CRUD** application is created when you run the **`start-app`** command.

## **CRUD**

All methods inside **`Query`** and **`Mutation`** classes are by default **static**-methods **`@staticmethod`**

Each function is turn into a **`@staticmethod`** when it gets loaded after the server starts running.

That means you don't use **`self`** inside your functions.

### Command

```sh
./manage.py start-app my_app --crud
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

### Classes

- **`Query`**: GraphQL "**Query**" functions.
- **`Mutation`**: GraphQL "**Mutation**" functions.
- **`Meta`**: **Configurations** for the current GraphQL functions.

### **Meta** Variables (**optional**)

- **`app`** (**bool**) : Prepend the **application**'s name to the operation's name.
- **`model`** (**str**): Prepend **model**'s name to the operation's name.

```text
root/
|
|--  apps/
|    `--  MY_APP/
|         `-- graphql/            --> <Directory> - Your GraphQL in HERE!
|             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
|             |-- demo.py         --> <File> - Demo File.
|             `-- etc...
|
`-- etc...
```

## Demo **Files**

=== "demo.py"

    ```python
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    # Fastberry
    import fastberry as fb


    # Create your API (GraphQL) here.
    @fb.gql
    class Demo:
        """Demo Api"""

        class Meta:
            """GQL-Class Metadata"""

            app = False
            model = "User"

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
