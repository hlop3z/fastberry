# GraphQL **API**

In this section we will learn about all the different available options to create **GraphQL** methods.

## **Import** your Basics

```python
from fastberry import Model # (1)
from fastberry import Text # (2)
from fastberry import JSON # (3)

from fastberry import GQL # (4)
from fastberry.graphql.inputs import Pagination # (5)
from fastberry.graphql.types import (
    Edges,
    Error,
    ErrorMessage,
    Mutation,
    Query,
    Response,
) # (6)
```

1. Base to **`create`** a **SQL**, **Mongo** or **Generic** **`{ Types }`**.
2. **Field:** Database **`Text`** and GraphQL **`String`**.
3. **Field:** Database **`JSON`** and GraphQL **`JSON`**.
4. Base **`class`** to create **`Query`** and **`Mutation`** methods.
5. **`Pagination`** method. Uses the **`manager.base.querying.items_per_page`** to **limit** the request.
6. Used for python **annotations**. Either for pure **`annotations`** or also to **`return`** a value that is **compliant** with your **GraphQL**

---

## Methods **Descriptions**

| Method         | Connects With ...                            | Description                                                                  |
| -------------- | -------------------------------------------- | ---------------------------------------------------------------------------- |
| **`Model`**    | Everything :material-emoticon-happy-outline: | Use **Model** to **create** custom **GraphQL** **`Type(s)`**                 |
| **`Edges`**    | **`Response`**                               | Use **Edges** for **`annotations`**                                          |
| **`Response`** | **`Edges`**                                  | Use **Response** to **`return`** a **list** of custom **GraphQL** **`Type`** |
| **`Error`**    | **`[ErrorMessage]`**                         | Use **Error** to **`return`** a **list** of **ErrorMessage**(s)              |
| **`Mutation`** | Type(**`CustomType`**)                       | Use **Mutation** for **`annotations`**                                       |
| **`Query`**    | Type(**`CustomType`**)                       | Use **Query** for **`annotations`**                                          |

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

    import strawberry

    # Create your <types> here.
    from fastberry import JSON, Model, Text

    model = Model()

    @model.type
    class Author:
        name: str

    @model.type
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


    @model.type
    class Category:
        name: str
    ```

=== "inputs.py"

    ```python title="inputs.py"
    # -*- coding: utf-8 -*-
    """
        API - Complex Inputs
    """

    import strawberry

    # Create your <inputs> here.
    @strawberry.input
    class SearchAuthor:
        name: str | None = None
    ```

=== "graphql.py"

    ```python title="graphql.py"
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    from fastberry import GQL
    from fastberry.graphql.inputs import Pagination
    from fastberry.graphql.types import (
        Edges,
        Error,
        ErrorMessage,
        Mutation,
        Query,
        Response,
    )

    from . import inputs, types


    class Demo(GQL):
        """Demo Api"""

        class Query:
            """Query"""

            async def detail() -> Query(types.Product):
                return types.Product(name="Model", aliases=["type", "class", "object"])

            async def single_instance(
                search: inputs.SearchAuthor | None
            ) -> Query(types.Author):
                return types.Author(_id=1, id=1, name="Ludwig Van Beethoven")

            async def multiple_instances(
                pagination: Pagination | None,
            ) -> Edges(types.Author):
                pagination = pagination or Pagination()
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
