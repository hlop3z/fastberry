from types import SimpleNamespace

from .ids import ID


def to_obj(items, sql: bool = False):
    """Convert Database-Based-Object into Python-SimpleNamespace-Object
    Args:
        items (list or dict): Database <Rows> or <Row>
        sql (bool, optional): IS-SQL Database? Defaults to False.
    """

    def row_handler(row: dict):
        # SQL-Alchemy
        row2dict = lambda row: {key: getattr(row, key) for key in row.keys()}
        if sql:
            row = row2dict(row)
        # Common
        unique_id = str(row["_id"])
        row["id"] = ID.encode(unique_id)
        if row:
            return SimpleNamespace(**row)
        return None

    def item_handler(rows):
        if isinstance(rows, list):
            # IF-List
            return [row_handler(i) for i in rows]
        # IF-Dict
        return row_handler(rows)

    if items:
        return item_handler(items)
    elif isinstance(items, list) and len(items) == 0:
        return []
    return None
