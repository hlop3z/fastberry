# GraphQL **API**

In this section we will learn about all the different available options to create **GraphQL** methods.

## **Import** your Basics

```python
from fastberry import BaseType # (1)
from fastberry import CRUD # (2)
from fastberry.graphql.inputs import Pagination # (3)
from fastberry.graphql.types import (
    Edges,
    Error,
    ErrorMessage,
    Mutation,
    Query,
    Response,
) # (4)
```

1. Base **`class`** for **`GraphQL`** **types**.
2. Base **`class`** to create **`Query`** and **`Mutation`** methods.
3. **`Pagination`** method. Uses the **`manager.base.querying.items_per_page`** to **limit** the request.
4. Used for python **annotations**. Either for pure **`annotations`** or also to **`return`** a value that is **compliant** with your **GraphQL**

---

## Responses

- **`Response`**
- **`Error`** + **`ErrorMessage`**

## Usage **Example**

=== "types.py"

    ```python title="types.py"
    # -*- coding: utf-8 -*-
    """
        API - Strawberry Types
    """

    import strawberry
    from fastberry import BaseType

    # Create your <types> here.
    @strawberry.type
    class Author(BaseType):
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

=== "crud.py"

    ```python title="crud.py"
    # -*- coding: utf-8 -*-
    """
        API - CRUD
    """

    from fastberry import CRUD
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


    class Demo(CRUD):
        """Demo Api"""

        class Query:
            """Query"""

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
