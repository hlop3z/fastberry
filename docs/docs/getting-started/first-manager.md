# First **Form**

Below is an example of a **`manager`** named "**`Book`**" that controls the **database `operations`**.

## Manager

```python title="apps/demo/manager.py"
# -*- coding: utf-8 -*-
"""
    { Controller } for the Database(s)
"""

import fastberry as fb

from . import types

# Create your <managers> here.
@fb.manager
class Book:
    """Product Manager"""

    model = types.Book

    @classmethod
    async def create(cls, form):
        # Errors
        errors_messages = []

        # Good Input
        if form.is_valid:
            results = await cls.objects.create(form.data.__dict__)
            if not results.error:
                item = results.data.__dict__
                return types.Book(**item)

        # Bad Input
        errors_messages.append(
            fb.error(type="input", text="Something Went Wrong!")
        )
        return fb.errors(messages=errors_messages)
```

## Usage

!!! info

    Go to the folder **`graphql`** inside your **demo** app.

    And, edit the method **`create`** to look like the example below.

```python title="apps/demo/graphql/demo.py"
# ETC . . .

# Type(s) Tools
from .. import forms, manager, types

@fb.gql
class Demo:
    class Meta:
        # ETC . . .

    class Query:
        # ETC . . .

    class Mutation:
        """Mutation"""

        async def create(form: forms.Book) -> fb.mutation(types.Book):
            """(Create-Book) Read the Docs"""
            return await manager.Book.create(form.input)

        # ETC . . .
```

## More at [Applications](../../applications/)

!!! warning

    **End of this tutorial**. To learn more about how to create **`Types`**, **`Forms`**, **`Manager`** and other **`functionalities`**.

    Please read the full documentation for the [Applications](../../applications/) section.
