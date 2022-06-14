> **Fields** that **translate** from a particular type between **`Python`** , **`SQL`** and **`GraphQL`** data.

## Model **Fields**

| GraphQL        | Python (Fastberry)      | SQLAlchemy         |
| -------------- | ----------------------- | ------------------ |
| **`ID`**       | **`str`**               | Integer            |
| **`String`**   | **`str`**               | String(length=255) |
| **`String`**   | **`fastberry.Text`**    | Text               |
| **`Integer`**  | **`int`**               | Integer            |
| **`Float`**    | **`float`**             | Float              |
| **`Boolean`**  | **`bool`**              | Boolean            |
| **`Datetime`** | **`datetime.datetime`** | DateTime           |
| **`Date`**     | **`datetime.date`**     | Date               |
| **`Time`**     | **`datetime.time`**     | Time               |
| **`Decimal`**  | **`decimal.Decimal`**   | Decimal            |
| **`JSON`**     | **`fastberry.JSON`**    | JSON               |

## Your **instance** includes **two** fields

1. **`_id` :** **(str)** Meant to be the **original** **`Database`** unique identifier.
2. **`id` :** **(str)** Meant to be the **client's** **`GraphQL`** unique identifier.

---

> **`ID`** is a special **Field** that represents the automatically created **`ID`** field for the database.
> You **won't use it** directly in your code.

## Python **Fields**

- **`str`**
- **`fastberry.Text`**
- **`int`**
- **`float`**
- **`bool`**
- **`datetime.datetime`**
- **`datetime.date`**
- **`datetime.time`**
- **`datetime.Decimal`**
- **`fastberry.JSON`**

## Usage **Example**

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
