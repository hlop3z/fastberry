# SQL-Alchemy **API**

In this section we will learn about all the available options to create **SQL-Queries**.
With the **SQLAlchemy `Manager`**.

## Connect **Table (Type)** to **Manager**

```python
from fastberry import SQLBase

DATABASE_URL = "sqlite:///test_database.db"

sql_manager = SQLBase(DATABASE_URL, My_Custom_GQL_Type)
```

### **Core** Methods

| Method                                                                           | Info                                                                |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| <a href="https://pypi.org/project/databases/" target="_blank">**`database`**</a> | **Databases** module. **Asyncio** support for a range of databases. |
| <a href="https://pypi.org/project/SQLAlchemy/" target="_blank">**`table`**</a>   | **SQLAlchemy** module. **Table** for a SQL-Database                 |
| **`Q`**                                                                          | **Custom-Querying** for **SQLAlchemy** Tables                       |

### **Read** Methods

| Method          | Is Used To...                                         | Variables                                   |
| --------------- | ----------------------------------------------------- | ------------------------------------------- |
| **`filter_by`** | **Filter-By** Columns (**Multiple**-Records)          | `(dict, page=1, limit=100, sort_by='-id' )` |
| **`search`**    | **Search** in Columns (**Multiple**-Records)          | `(list[str(columns)], page=1, etc...)`      |
| **`find`**      | **Custom-Querying** (**Multiple**-Records)            | `(custom_query, page=1, etc...)`            |
| **`get_by`**    | **Filter-By** Columns (**Single**-Record)             | `(**kwargs)`                                |
| **`detail`**    | Get **Details** by **GraphQL-ID** (**Single**-Record) | `(GraphQL_ID)`                              |

### **C.U.D** Methods

| Method       | Is Used To...                                                                        | Variables          |
| ------------ | ------------------------------------------------------------------------------------ | ------------------ |
| **`form`**   | **Clean** User's **`Inputs`**. And, **only** allows fields that are in the DataBase. | `(dict)`           |
| **`create`** | **Create** a Single-Records.                                                         | `(dict)`           |
| **`update`** | **Edit** Multiple-Records.                                                           | `(list[ID], dict)` |
| **`delete`** | **Delete** Multiple-Records.                                                         | `(list[ID])`       |

### **Custom-Querying** Methods

> **Usage**: `Q.where(str: "column", str: "operation", Any: value)`

For **Example**: `sql_manager.Q.where("id", "in", [1, 2, 3])`

| Method         | Is Used To...                        |
| -------------- | ------------------------------------ |
| **`eq`**       | **Equals**                           |
| **`ne`**       | **Not Equals**                       |
| **`lt`**       | **Less than**                        |
| **`le`**       | **Less than or Equal than**          |
| **`gt`**       | **Greater than**                     |
| **`ge`**       | **Greater than or Equal than**       |
| **`contains`** | **Custom Text Search (Ignore-Case)** |
| **`like`**     | **Text Search "%" (Case-Sensitive)** |
| **`ilike`**    | **Text Search "%" (Ignore-Case)**    |
| **`in`**       | **In List**                          |
| **`bt`**       | **Between** "A & B"                  |
