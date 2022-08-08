> Your code **needs** to be in a **file** named **`types.py`** inside your **Application**.

The **database** layout is **optional**. You can start your model base anywhere you will like.

## File **Layout**

=== ":material-file: Types (Models)"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- types.py                --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-file: Databases"

    ``` text
    root/
    |
    |--  project/
    |    `--  databases/
    |         |-- __init__.py             --> <File> - Your MODEL instance in HERE!
    |         |-- sql.py                  --> <File> - SQL
    |         `-- mongo.py                --> <File> - Mongo
    |
    `-- etc...
    ```

> Both **`Mongo`** and **`SQLAlchemy`** are **optional**. But I do recommend using **at least one**. Otherwise, there is **no point** in using this section and **instead** you should just declare your **`Types`** by using <a href="https://strawberry.rocks/docs/types/object-types/" target="_blank" rel="noopener noreferrer">**Strawberry**</a>

## Python **Code**

=== "Types"

    ```python title="types.py"
    # -*- coding: utf-8 -*-
    """
        Types
    """


    import dataclasses as dc
    import datetime
    import decimal
    import typing

    import fastberry as fb

    from project.databases import model

    # DateTime Functions
    class Date:
        datetime = lambda: datetime.datetime.now()
        date = lambda: datetime.date.today()
        time = lambda: datetime.datetime.now().time()

    # Create your <types> here.
    @model.sql
    class Product:
        name: str
        aliases: list[str] | None = None
        stock: int | None = None
        is_available: bool | None = None
        created_on: datetime.datetime = dc.field(default_factory=Date.datetime)
        available_from: datetime.date = dc.field(default_factory=Date.date)
        same_day_shipping_before: datetime.time = dc.field(default_factory=Date.time)
        price: decimal.Decimal | None = None
        notes: list[fb.Text] = dc.field(default_factory=list)
        is_object: fb.JSON = dc.field(default_factory=dict)

        async def category(self) -> typing.Optional["Category"]:
            return Category(name="awesome")


    @model.sql
    class Category:
        name: str
    ```

=== "Databases"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
        Databases
    """

    import fastberry

    from .mongo import Base as Mongo
    from .sql import Base as Sql

    model = fastberry.Model(sql=Sql, mongo=Mongo)
    ```

=== "SQL"

    ```python title="sql.py"
    # -*- coding: utf-8 -*-
    """
        SQL
    """

    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base

    # Config
    DATABASE_URL = "sqlite:///test_database.db"

    # Engine
    ENGINE = create_engine(DATABASE_URL, echo=True)


    # Base
    Base = declarative_base()
    ```

=== "Mongo"

    ```python title="mongo.py"
    # -*- coding: utf-8 -*-
    """
        Mongo
    """

    import motor.motor_asyncio

    # Config
    DATABASE_URL = "mongodb://localhost:27017"
    DATABASE_NAME = "test_database"

    # Engine
    ENGINE = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


    # Base
    Base = ENGINE[DATABASE_NAME]
    ```
