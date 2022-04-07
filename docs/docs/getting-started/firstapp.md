## App Layout

---

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

## Inputs, Models & Types

=== "inputs.py"

    ```python
    # Strawberry
    import strawberry


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

=== "models.py"

    ```python
    # Fastberry
    from fastberry import Database

    # Database Manager
    model = Database()

    # Create your <models> here.
    Author = model.motor("Author")

    # Create Index For Collection(s)
    def create_indexes():
        model.mongo["author"].create_index([("name", 1)], unique=True)

    ```

=== "types.py"

    ```python
    # Strawberry
    import strawberry

    # Fastberry
    from fastberry import BaseType

    # Create your <types> here.
    @strawberry.type
    class Author(BaseType):
        name: str
    ```

---

## CRUD

### Variables (optional)

- **`schema`**: Requires a **type &lt;`strawberry.type`&gt;**.
- **`prefix`**: A prefix(**str**) to use before the function name.

### Classes

- **`Query`**: GraphQL "**Query**" functions.
- **`Mutation`**: GraphQL "**Mutation**" functions.

### Files

=== "demo.py"

    ```python
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
    from .demo import Demo
    ```
