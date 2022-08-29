import dbcontroller as dbc

from .. import Form


@Form.read("name_of_my_search")
class Search:
    name = dbc.field(str, default="Hello World")

    class Method:
        def run(self):
            return self.name
