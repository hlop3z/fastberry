# First **Form**

!!! info "First Type"

    Below is an example of a **`form`** named "**`Book`**" that contains **(2) two fields**

    - **`title`**
    - **`author`**

    Just like our **First Type**.

## Form

```python title="apps/demo/forms.py"
# -*- coding: utf-8 -*-
"""
    { Forms } for GraphQL
"""
import fastberry as fb

# Create Group "Form"
form = fb.input("form")

# Create your <forms> here.
@form
class Book:
    """(FormBook) Read The Docs"""

    title = fb.value(
        str,
        default=None,
        required=True
    )
    author = fb.value(
        str,
        default=None,
        required=True
    )
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

            # Client's Input
            print(form.input)

            # Return a "Book" Type
            return types.Book(
                id="encoded_id",
                author="F. Scott Fitzgerald",
                title="The Great Gatsby"
            )

        # ETC . . .
```

!!! note "In the Browser"

    Go to <a href="http://127.0.0.1:8000/graphql" target="_blank">**http://127.0.0.1:8000/graphql**</a>
    And **paste the code** from below.

    Then, "**Execute Query**" by pressing the ":material-play-box:" play button.

## GraphQL (**Mutation**)

```
mutation MyMutation {
  create(form: {
    author: "F. Scott Fitzgerald",
    title: "The Great Gatsby"
  }) {
    ... on Book {
      id
      title
      author
    }
    ... on Error {
      error
      meta
      messages {
        field
        text
        type
      }
    }
  }
}
```

## Terminal "**Print**"

!!! info

    Go to your **terminal** and look at the output.

<div id="terminal-getting-started-first-form" data-termynal></div>
