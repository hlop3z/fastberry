# SQL - **Querying**

## **SQL**Alchemy

> Start by creating the **Basics** of your database **Controller**

```python
from fastberry import Model # (1)
from sqlalchemy.orm import declarative_base # (2)

# Config
DATABASE_URL = "sqlite:///test_database.db"

# Base
Base = declarative_base()

# Models
model = Model(sql=Base)
```

1. Each **model** maps to a single database **(Table | Collection)**.
2. **SQLAlchemy** — Model's Base.

---

## **Manager**

> Create a reusable **Manager**

```python
from fastberry import SQLBase

def SQL(table):
    """SQL Manager"""
    return SQLBase(DATABASE_URL, table)
```

---

## Create **Table (Type)**

> Define a `database` **Table** (aka: `GraphQL` **Type**).

```python
@model.sql
class Category:
    name: str
```

## Connect **Table (Type)** to **Manager**

```python
sql_manager = SQL(Category)
```

## Usage **Example** more at ... [API - References](/fastberry/apis/sqlalchemy/)

```python
# Usage
async def create_category():
    input_form = sql_manager.form(
        {
            "name": "Awesome",
        }
    )
    results = await sql_manager.create(input_form)
    print(results)

# Test
await create_category()
```
