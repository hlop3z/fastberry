# GraphQL **API**

In this section we will learn about all the available options to create **GraphQL** methods.

## **Import** your Basics

```python
from fastberry import Model # (1)
from fastberry import Text # (2)
from fastberry import JSON # (3)

from fastberry import GQL # (4)
from fastberry.graphql.inputs import Pagination # (5)
from fastberry import edges, error, errors, mutation, page, query # (6)
```

1. Base to **`create`** a **SQL**, **Mongo** or **Generic** **`{ Types }`**.
2. **Field:** Database **`Text`** and GraphQL **`String`**.
3. **Field:** Database **`JSON`** and GraphQL **`JSON`**.
4. Base **`class`** to create **`Query`** and **`Mutation`** methods.
5. **`Pagination`** method. Used to **limit** the request.
6. Used for python **annotations**. Either for pure **`annotations`** or also to **`return`** a value that is **compliant** with your **GraphQL**

---

## Methods **Descriptions**

| Method         | Connects With ... | Description                                                              |
| -------------- | ----------------- | ------------------------------------------------------------------------ |
| **`errors`**   | **`[error]`**     | Use **errors** to **`return`** a **list** of **error**(s)                |
| **`mutation`** | **`Types`**       | Use **mutation** for **`annotations`**                                   |
| **`query`**    | **`Types`**       | Use **query** for **`annotations`**                                      |
| **`edges`**    | **`page`**        | Use **edges** for **`annotations`**                                      |
| **`page`**     | **`[edges]`**     | Use **page** to **`return`** a **list** of custom **GraphQL** **`Type`** |

| Method      | Connects With ...                            | Description                                                  |
| ----------- | -------------------------------------------- | ------------------------------------------------------------ |
| **`Model`** | Everything :material-emoticon-happy-outline: | Use **Model** to **create** custom **GraphQL** **`Type(s)`** |

## Usage **Example**

=== "types.py"

    > **Model(s)** is **`optional`** and it has **2 Required Fields**.

    1. **`_id` :** **(str)** Meant to be the **original** **`Database`** unique identifier.
    2. **`id` :** **(str)** Meant to be the **client's** **`GraphQL`** unique identifier.

    ```python title="types.py"
    # -*- coding: utf-8 -*-
    """
        API - Strawberry Types
    """

    import datetime
    import decimal
    import typing

    # Create your <types> here.
    import fastberry as fb

    @fb.mongo.model
    class Author:
        """(Type) Read The Docs"""
        name: str

    @fb.sql.model(description="(Type) Read The Docs")
    class Product:
        """
        query MyQuery {
            demoDetail {
                name
                aliases
                stock
                isAvailable
                createdAt
                sameDayShippingBefore
                price
                notes
                isObject
                category {
                    name
                }
            }
        }
        """
        name: str
        aliases: list[str] | None = None
        stock: int | None = None
        is_available: bool | None = None
        available_from: datetime.date | None = None
        created_at: datetime.datetime | None = None
        same_day_shipping_before: datetime.time | None = None
        price: decimal.Decimal | None = None
        notes: list[Text] = dc.field(default_factory=list)
        is_object: JSON = dc.field(default_factory=dict)

        async def category(self) -> typing.Optional["Category"]:
            return Category(name="awesome")


    @fb.sql.model
    class Category:
        """(Type) Read The Docs"""
        name: str
    ```

=== "inputs.py"

    ```python title="inputs.py"
    # -*- coding: utf-8 -*-
    """
        API - Complex Inputs
    """
    import fastberry as fb

    # Create Group "Form"
    form = fb.input("form")

    # Create your <forms> here.
    @form
    class Search:
        """(Form) Read The Docs"""

        email = fb.value(
            str,
            default="demo@helloworld.com",
            regex={
                r"[\w\.-]+@[\w\.-]+": "invalid email address"
            },
            rules=[
                (lambda v: v.startswith("demo") or "invalid input")
            ],
            filters=fb.filters(
                regex=[
                    ("^hello", "hola"),
                    ("com", "api"),
                ],  # ("^hello"...) [Won't Work]: We used { regex } to check if it startswith "hello".
                rules=[
                    (lambda v: v.upper())
                ],
            ),
        )
    ```

=== "graphql.py"

    ```python title="graphql.py"
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    from fastberry.graphql.inputs import Pagination
    import fastberry as fb

    from .. import forms, manager, types

    @fb.gql
    class Demo:
        """Demo Api"""

        class Query:
            """Query"""

            async def detail() -> fb.query(types.Product):
                return types.Product(name="Model", aliases=["type", "class", "object"])

            async def single_instance(
                search: inputs.SearchAuthor | None
            ) -> fb.query(types.Author):
                return types.Author(_id=1, id=1, name="Ludwig Van Beethoven")

            async def multiple_instances(
                search: forms.Search,
                pagination: fb.pagination,
            ) -> fb.edges(types.Author):
                print(pagination)
                print(search.input)
                return Response(
                    edges=[
                        types.Author(_id=1, id=1, name="Ludwig Van Beethoven"),
                        types.Author(_id=2, id=2, name="Wolfgang Amadeus Mozart"),
                    ],
                    length=2,
                    pages=1,
                )

        class Mutation:
            """Mutation"""

            async def create_good() -> Mutation(types.Author):
                if True:
                    return types.Author(_id=2, id=2, name="Wolfgang Amadeus Mozart")
                return None

            async def create_bad() -> Mutation(types.Author):
                if False:
                    return None
                return Error([ErrorMessage(type="input", message="invalid input.")])

    ```

=== "GraphQL"

    ```graphql
    query Item {
        singleInstance(search: null) {
            id
            name
        }
    }

    query List {
        multipleInstances(pagination: null) {
            edges {
                node {
                    id
                    name
                }
            }
        }
    }

    mutation createGood {
        createGood {
            ... on Author {
                id
                name
            }
            ... on Error {
                messages {
                    type
                    message
                }
            }
        }
    }

    mutation createBad {
        createBad {
            ... on Author {
                id
                name
            }
            ... on Error {
            error
                messages {
                    type
                    message
                }
            }
        }
    }
    ```
