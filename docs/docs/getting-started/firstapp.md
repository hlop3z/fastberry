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

=== "models.py"

    > **Models** map to a single database table (**SQL**) or database collection (**Mongo**).

    - **SQL** : Pairs with **SQLAlchemy**
    - **Mongo** : Pairs with (**Motor & PyMongo**)

    > **SQLAlchemy** uses the ORM syntax. While **Mongo** is just the name of the collection you want to interact with.

    === "SQL"

        ``` python
        # -*- coding: utf-8 -*-
        """
            Models
        """

        # SQLAlchemy
        from sqlalchemy import Column, Integer, String
        from sqlalchemy.orm import declarative_base

        # Fastberry
        from fastberry import Database

        # (Base) SQLAlchemy
        Base = declarative_base()

        # Database Manager
        model = Database()

        # Create your <models> here.
        class AuthorDB(Base):
            """Database Model"""

            __tablename__ = "Author"

            id = Column(Integer, primary_key=True)
            name = Column(String(80))


        # Register your <models> here.
        Author = model.sql(AuthorDB)
        ```

    === "Mongo"

        ``` python
        # -*- coding: utf-8 -*-
        """
            Models
        """

        # Fastberry
        from fastberry import Database

        # Database Manager
        model = Database()

        # Create your <models> here.
        Author = model.motor("Author")

        # Create Index For Collection(s)
        def create_indexes():
            """Create Collection Indexes"""
            model.mongo["author"].create_index([("name", 1)], unique=True)
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
