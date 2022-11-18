> Your code **needs** to be in a **file** named **`graphql.py`** or **folder** named **`graphql`** inside your **Application**.

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- graphql.py            --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- graphql/            --> <Directory> - Your GraphQL in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

## Python **Code**

=== ":material-file: File"

    ``` python title="graphql.py"
    # -*- coding: utf-8 -*-
    """
        API - GraphQL
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
            model = None

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
        GraphQL - Init
    """

    # Import your <cruds> here.
    from .demo import Demo
    ```

    ``` python title="demo.py"
    # -*- coding: utf-8 -*-
    """
        API - GraphQL
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
            model = None

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
