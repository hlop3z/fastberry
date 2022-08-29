import dbcontroller as dbc
from .. import Form

@Form.create
class Create:
    name = dbc.field(
        str,
        filters=dbc.filters(
            rules=[lambda v: float(v)],
        ),
    )


@Form.update
class Update:
    name = dbc.field(str)


@Form.delete
class Delete:
    name = dbc.field(str)