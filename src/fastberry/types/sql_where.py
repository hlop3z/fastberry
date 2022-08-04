"""
    * SQL-Querying
"""

import functools
from collections import namedtuple
from typing import Any

# SQLAlchemy
try:
    import sqlalchemy as sa
    from sqlalchemy.sql.elements import BinaryExpression
except ImportError:
    sa = None
    BinaryExpression = None


Page = namedtuple("Page", ["offset", "limit"])
QueryCount = namedtuple("QueryCount", ["query", "count"])


def pagination(page: int = 1, limit: int = 100):
    """Database Pagination."""
    # Clean Input
    _page = page if page > 0 else 1
    _limit = limit if limit > 0 else 1
    # Pagination
    offset = (_page - 1) * _limit
    return Page(offset, _limit)


def sql_where_base(table, key: str, operation: str, val: Any):
    """SQL-WHERE Single-Column Operator

    -----------------------------------------------------------------------------------------------
    # Usage
    -----------------------------------------------------------------------------------------------
    - where(str: "column", str: "operation", Any: value)

    -----------------------------------------------------------------------------------------------
    # Operations
    -----------------------------------------------------------------------------------------------
    - eq        : Equals
    - ne        : Not Equals
    - lt        : Less than
    - le        : Less than or Equal than
    - gt        : Greater than
    - ge        : Greater than or Equal than
    - contains  : Custom Text Search (Ignore-Case)
    - like      : Database Text Search "%" (Case-Sensitive)
    - ilike     : Database Text Search "%" (Ignore-Case)
    - in        : In List
    - bt        : Between "A & B"
    """
    return_value = None
    col = None
    found = False
    is_not = False
    if operation.startswith("!"):
        operation = operation[1:]
        is_not = True
    if hasattr(table.c, key):
        col = getattr(table.c, key)
        found = True
    # Operator
    if found:
        match operation:
            case "eq":
                sql_ope = getattr(col, "__eq__")
                return_value = sql_ope(val)
            case "ne":
                sql_ope = getattr(col, "__ne__")
                return_value = sql_ope(val)
            case "lt":
                sql_ope = getattr(col, "__lt__")
                return_value = sql_ope(val)
            case "le":
                sql_ope = getattr(col, "__le__")
                return_value = sql_ope(val)
            case "gt":
                sql_ope = getattr(col, "__gt__")
                return_value = sql_ope(val)
            case "ge":
                sql_ope = getattr(col, "__ge__")
                return_value = sql_ope(val)
            case "contains":
                sql_ope = getattr(col, "contains")
                return_value = sql_ope(val)
            case "like":
                sql_ope = getattr(col, "like")
                return_value = sql_ope(val)
            case "ilike":
                sql_ope = getattr(col, "ilike")
                return_value = sql_ope(val)
            case "in":
                sql_ope = getattr(col, "in_")
                return_value = sql_ope(val)
            case "bt":
                sql_ope = getattr(col, "between")
                return_value = sql_ope(*val)
    if is_not:
        return_value = sa.not_(return_value)
    return return_value


class Filters:
    """SQL-Querying

    -----------------------------------------------------------------------------------------------
    # Init
    -----------------------------------------------------------------------------------------------
    Q = Filters(SQlAlchemyORM.__table__)

    -----------------------------------------------------------------------------------------------
    # Methods
    -----------------------------------------------------------------------------------------------
    - SQL-Where      : Q.where("id", "in", [1, 2, 3])
    - Filter-By      : Q.filter_by(id=1, name="spongebob")
    - Search-Columns : Q.search(["name", "title"], "bob")

    -----------------------------------------------------------------------------------------------
    # Compiling
    -----------------------------------------------------------------------------------------------
    - Compile-Query  : Q.select(Q.search(["name", "title"], "bob"))
    - Custom-Querying: Q.find(Q.filter_by(name="bob"), page=1, limit=100, sort_by='-id')
    """

    def __init__(self, objects):
        sql_where = functools.partial(sql_where_base, objects)

        def querying(query: BinaryExpression | None = None):
            """SQL-Querying"""
            if isinstance(query, BinaryExpression):
                return objects.select().where(query)
            return objects.select()

        def search(columns: list, search: str):
            """Filter By X-Word"""
            query = None
            if columns:
                query = sql_where(columns[0], "contains", search)
                for col in columns[1:]:
                    query |= sql_where(col, "contains", search)
            return query

        def filter_by(**kwargs):
            """Filter By X-Column"""
            query = None
            items = [(key, "eq", val) for key, val in kwargs.items()]
            if items:
                query = sql_where(*items[0])
                for item in items[1:]:
                    query &= sql_where(*item)
            return query

        def sql_count(search: Any = None):
            """Get Query's Count"""
            total_count = sa.select([sa.func.count()])
            if isinstance(search, BinaryExpression):
                total_count = total_count.where(search)
            return total_count.select_from(objects)

        def sort_by_column_base(sort_by: str = None):
            """Sort-By X-Column"""
            sort_desc = False
            sort_by_col = None
            if sort_by:
                # Sort By (Descending || Ascending)
                if sort_by.startswith("-"):
                    sort_by = sort_by[1:]
                    sort_desc = True
                # Check Sort By
                if sort_by:
                    if hasattr(objects.c, sort_by):
                        sort_by_col = getattr(objects.c, sort_by)
                    else:
                        sort_by_col = objects.c.id
                # Add Sort Desc
                if sort_desc:
                    sort_by_col = sa.desc(sort_by_col)
            return sort_by_col

        def sort_by_column(query, sort_by: str = None):
            """Sort-By X-Column"""
            return query.order_by(sort_by_column_base(sort_by))

        def sql_pagination(query, page: int = 1, limit: int = 100):
            """Pagination"""
            _page = pagination(page=page, limit=limit)
            return query.offset(_page.offset).limit(_page.limit)

        def sql_find(
            search: BinaryExpression = None,
            page: int | None = None,
            limit: int | None = None,
            sort_by: str | None = None,
        ):
            """Pagination and Sort-By"""
            query = querying(search)
            if sort_by:
                query = sort_by_column(query, sort_by)
            if page and limit:
                query = sql_pagination(query, page=page, limit=limit)
            return query

        def sql_find_and_count(
            search: BinaryExpression = None,
            page: int | None = None,
            limit: int | None = None,
            sort_by: str | None = None,
        ):
            """Find and Count"""
            count = sql_count(search)
            query = sql_find(search, page=page, limit=limit, sort_by=sort_by)
            return QueryCount(query=query, count=count)

        # Definitions
        self.select = querying
        self.where = sql_where
        self.search = search
        self.filter_by = filter_by
        self.find = sql_find_and_count
