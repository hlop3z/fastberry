## **Mongo** or **SQL**

> You can create more **Advanced** Model configurations for your SQL-Database(s) **Tables**.

## Specific **Database** Controller

=== "SQLAlchemy"

    ```python title="with_sql.py"
    # -*- coding: utf-8 -*-
    """
        SQLAlchemy
    """

    from project.databases import model

    @model.sql
    class Product:
        name: str
    ```

=== "Mongo"

    ```python title="with_mongo.py"
    # -*- coding: utf-8 -*-
    """
        Mongo
    """

    from project.databases import model

    @model.mongo
    class Product:
        name: str
    ```

## Database **Model** Setup

| Key                   | Description                                                         |
| --------------------- | ------------------------------------------------------------------- |
| **`table_name`**      | (**`str`**) — Custom **Table Name** for the database                |
| **`primary_key`**     | (**`list[str]`**) — Columns that are consider **Primary Key**       |
| **`required`**        | (**`list[str]`**) — Columns that **Required** User's input          |
| **`index`**           | (**`list[str]`**) — Columns that are **Index**                      |
| **`unique`**          | (**`list[str]`**) — Columns that are **Unique**                     |
| **`unique_together`** | (**`list[tuple]`**) — Group of Columns that are **Unique Together** |
| **`many_to_many`**    | (**`list[str]`**) — Columns that relate and are **Many-To-Many**    |

> **Note:** the **`many_to_many`** field is **ONLY** used for information purposes currently it doesn't handle that part automatically.

## Usage **Example**

> The configurations are for the **SQL-Database (ONLY)** to configure the **Model / Type** just use regular **Typing** annotations.

```python title="model-setup-sample.py"
# -*- coding: utf-8 -*-
"""
    Model-Setup-Sample
"""

from project.databases import model

@model.sql(
    table_name="custom_table_name",
    primary_key=["col_one"],
    required=["col_one"],
    index=["col_one"],
    unique=["col_one"],
    unique_together=[("col_one", "col_two")],
    many_to_many=["col_one"],
)
class Product:
    name: str
```
