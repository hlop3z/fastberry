"""
    * SQLAlchemy + Databases — Controller
"""

import functools
import math
from types import SimpleNamespace
from typing import Any

from .sql_where import Filters as SQLFilters
from .utils import sql_id_decode, to_obj

try:
    from sqlalchemy.sql.elements import BinaryExpression
except ImportError:
    BinaryExpression = None

try:
    from databases import Database
except ImportError:
    Database = lambda x: SimpleNamespace(database_url=x)


def sql_response(
    data: Any = None,
    error: bool = False,
    error_message: str | None = None,
    count: int | None = None,
    pages: int | None = None,
):
    """Database Transaction Response"""
    return SimpleNamespace(
        data=data, error=error, error_message=error_message, count=count, pages=pages
    )


def clean_form(base: Any, cols: list, form: dict):
    """Clean User's Input

    Args:
        form (dict): User's Input.

    Returns:
        dict: Clean User's Input.
    """
    inputs = {}
    base_form = base(**form)
    for key, val in base_form.__dict__.items():
        if key in cols and key != "_id":
            inputs[key] = val
    return inputs


def clean_update_form(base: Any, cols: list, form: dict):
    clean = clean_form(base, cols, form)
    return {key: val for key, val in clean.items() if val}

# Testing
class SQLBase:
    """SQlAlchemy & Databases (Manager)

    -----------------------------------------------------------------------------------------------
    # Init
    -----------------------------------------------------------------------------------------------
    sql = SQLBase(database_url, custom_type)

    -----------------------------------------------------------------------------------------------
    # Form
    -----------------------------------------------------------------------------------------------
    - Clean-Inputs      : sql.form(dict)
    - Clean-Empty       : sql.form_update(dict)

    -----------------------------------------------------------------------------------------------
    # Read (Examples)
    -----------------------------------------------------------------------------------------------
    - Filter-By         : await sql.filter_by(id=1, name="spongebob")
    - Search-Columns    : await sql.search(["name", "title"], "bob")
    - Get-By(Single-Row): await sql.get_by(id=1, name="spongebob")
    - Custom-Querying   : await sql.find(
                                    sql.Q.where("id", "in", [1, 2, 3]),
                                    page=1, limit=100, sort_by='-id'
                                )

    -----------------------------------------------------------------------------------------------
    # C.U.D
    -----------------------------------------------------------------------------------------------
    - Create            : await sql.create(dict)
    - Update            : await sql.update(items: list[IDs], values: dict)
    - Delete            : await sql.delete(items: list[IDs])
    """

    def __init__(self, database_url, custom_type):
        """Start Manager"""
        self.database = Database(database_url)
        self.table = custom_type.objects
        self.Q = SQLFilters(custom_type.objects)
        self.form = functools.partial(clean_form, custom_type, custom_type.objects.columns.keys())
        self.form_update = functools.partial(clean_update_form, custom_type, custom_type.objects.columns.keys())

    async def find(
        self,
        search: BinaryExpression = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
    ):
        """Get Multiple-Rows from Database Table by <SQLAlchemy-BinaryExpression>"""
        try:
            query = self.Q.find(search, page=page, limit=limit, sort_by=sort_by)
            items = await self.database.fetch_all(query.query)
            count = await self.database.fetch_val(query.count)
            _limit = limit or 1
            pages = int(math.ceil(count / _limit))
            return sql_response(data=to_obj(items, sql=True), count=count, pages=pages)
        except:
            return sql_response(data=[], count=0, pages=0)

    async def filter_by(
        self,
        search: dict | None = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
    ):
        """Get Multiple-Rows from Database Table by <Keyword-Arguments>"""
        query = self.Q.filter_by(**search) if search else None
        items = await self.find(query, page=page, limit=limit, sort_by=sort_by)
        return items

    async def search(
        self,
        columns: list | None = None,
        value: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
    ):
        """Get Multiple-Rows from Database Table by <Searching-Columns>"""
        query = self.Q.search(columns, value) if value else None
        items = await self.find(query, page=page, limit=limit, sort_by=sort_by)
        return items

    async def get_by(self, **kwargs):
        """Get Single-Row from Database Table by <Keyword-Arguments>"""
        query = self.Q.filter_by(**kwargs)
        item = await self.database.fetch_one(self.Q.select(query))
        return to_obj(item, sql=True)

    async def detail(self, ID):
        """Get Single-Row from Database ID"""
        query = self.Q.filter_by(_id=sql_id_decode(ID))
        item = await self.database.fetch_one(self.Q.select(query))
        return to_obj(item, sql=True)

    async def create(self, form: dict):
        """Create Single-Row."""
        # Init Values
        return_value = sql_response()
        unique_id = False
        try:
            sql_query = self.table.insert(form)
            unique_id = await self.database.execute(sql_query)
            if unique_id:
                # If Success => Fetch Row
                return_value.data = await self.get_by(_id=unique_id)
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)

        return return_value

    async def update(self, unique_ids: list[str], **kwargs):
        """Update Multiple/Single-Row(s)"""
        return_value = sql_response()
        # Get Ids
        all_ids = [sql_id_decode(i) for i in unique_ids]
        sql_ids_in = self.Q.where("_id", "in", all_ids)
        try:
            return_value.count = await self.database.execute(
                self.table.update().where(sql_ids_in).values(**kwargs)
            )
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        # Get Details
        if len(all_ids) == 1 and return_value.count == 1:
            return_value.data = await self.get_by(_id=all_ids[0])
        return return_value

    async def delete(self, unique_ids: list[str]):
        """Delete Multiple/Single-Row(s)"""
        return_value = sql_response()
        # Get Ids
        all_ids = [sql_id_decode(i) for i in unique_ids]
        sql_ids_in = self.Q.where("_id", "in", all_ids)
        try:
            return_value.count = await self.database.execute(
                self.table.delete().where(sql_ids_in)
            )
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        return return_value
