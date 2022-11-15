"""
    { Operations } for GraphQL
"""
import fastberry as fb

# Import Once's per project in any App.
# IF you want the built-in (Forms) to be register in the GraphQL API.
from fastberry import item, pagination

form = fb.input("form")

@form
class Category:
    """(Form) Read The Docs"""

    name = fb.value(
        str,
        required=True,
    )

@form(name="SearchEngine")
class Search:
    """(Form) Read The Docs"""

    name = fb.value(
        str,  # Single Typing
        default=None,
    )
    count = fb.value(
        int,
        default=None,
    )    
    cash = fb.value(
        float,
        default=None,
    )
    amount = fb.value(
        fb.decimal,
        default=None,
    )
    start_date = fb.value(
        fb.date,
        default=None,
    )
    end_datetime = fb.value(
        fb.datetime,
        default=None,
    )
    timestamp = fb.value(
        fb.time,
        default=None,
        required=False,
    )
