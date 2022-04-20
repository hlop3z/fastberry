## App **Layout**

```text
my-app/                 --> <Directory> - Your App Root Directory.
|
|--  crud/              --> <Directory> - Your API's CRUD(s) Code in HERE.
|    |-- __init__.py    --> <File> - Import All Your CRUD Models in HERE.
|    `-- demo.py        --> <File> - CRUD Model Demo.
|
|--  operations/        --> <Directory> - Your GraphQL's Operations in HERE.
|    |-- core/          --> <File> - Use in both (Desktop & Mobile).
|    |-- desktop/       --> <File> - Use in Desktop.
|    `-- mobile/        --> <File> - Use in Mobile.
|
|-- __init__.py
|-- inputs.py           --> <File> - GraphQL Inputs.
`-- types.py            --> <File> - GraphQL Types.
```

---

### Create App **Command**

```sh
./manage.py start-app my_app --crud
```

---

=== "inputs.py"

    > "**Input types** cannot have fields that are other objects, **only** basic scalar types, list types, and other input types". — **graphql.org**

    ``` python
    # -*- coding: utf-8 -*-
    """
        Inputs
    """

    # Strawberry
    import strawberry


    # Create your <inputs> here.
    @strawberry.input
    class SearchAuthor:
        name: str | None = None

        def init(self):
            """Add Search Parameters to Query"""

            query = {}
            if self.name:
                query["name"] = {"$regex": self.name}

            return query

    ```

=== "types.py"

    > "**Object types**, which just represent a kind of object you can fetch from your service, and what fields it has". — **graphql.org**

    ``` python
    # -*- coding: utf-8 -*-
    """
        Types
    """

    # Strawberry
    import strawberry

    # Fastberry
    from fastberry import BaseType

    # Create your <types> here.
    @strawberry.type
    class Author(BaseType):
        name: str
    ```

=== "demo.py"

    ``` python
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

    ``` python
    # -*- coding: utf-8 -*-
    """
        CRUD - Init
    """

    from .demo import Demo
    ```
