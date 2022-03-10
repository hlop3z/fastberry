import datetime
import decimal
import enum
import json
import pathlib
import re
import uuid
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from project.settings import BASE_DIR


def get_operations(query):
    Substring = "(query \w+|mutation \w+)"
    operations = [
        f.replace("query", "").replace("mutation", "").strip()
        for f in re.findall(Substring, query, re.IGNORECASE)
    ]
    return sorted(operations)


def role_operations():
    all_roles = {}
    root = BASE_DIR / "roles"
    for path in pathlib.Path(root).glob("*"):
        role_query = ""
        if path.is_dir():
            for file in path.glob("*.graphql"):
                with open(file, "r") as f:
                    role_query += "\n"
                    role_query += f.read()
            all_roles[path.name] = role_query
    return all_roles


class Roles:
    def __init__(self, schema=None):
        # Roles
        roles = role_operations()

        # Operations
        __operations__ = list(
            set(get_operations("\n".join([f for f in roles.values()])))
        )
        operations = enum.Enum("Operations", {k: k for k in __operations__})

        # Init: Setup
        self.schema = schema
        self.roles = roles
        self.all_operations = operations
        self._all_operations = __operations__

    def operations(self, role=None):
        query = self.roles.get(role)
        if query:
            ops = get_operations(query)
        else:
            ops = None
        return ops

    def execute_sync(self, role=None, operation=None, variables=None):
        query = self.roles.get(role)
        if operation in query and query:
            resp = self.schema.execute_sync(
                query,
                operation_name=operation,
                variable_values=variables,
            )
            return dict(data=resp.data, errors=resp.errors)
        return None

    async def execute(self, role=None, operation=None, variables=None):
        query = self.roles.get(role)
        if query and operation in query:
            resp = await self.schema.execute(
                query,
                operation_name=operation,
                variable_values=variables,
            )
            return dict(data=resp.data, errors=resp.errors)
        return None


@dataclass
class Instance:
    value: Any = None
    default: Any = None
    required: bool = False
    isObject: bool = False
    type: str = None


class NestedNamespace(SimpleNamespace):
    @staticmethod
    def map_entry(entry):
        if isinstance(entry, dict):
            return NestedNamespace(**entry)

        return entry

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, val in kwargs.items():
            if type(val) == dict:
                setattr(self, key, NestedNamespace(**val))
            elif type(val) == list:
                setattr(self, key, list(map(self.map_entry, val)))


def try_json(value):
    try:
        return json.loads(value)
    except:
        return value


SCALAR_TYPES = [
    "String",
    "Int",
    "Float",
    "Boolean",
    "ID",
    "Date",
    "DateTime",
    "Time",
    "Decimal",
    "UUID",
    "Void",
]


def get_scalar_type(value):
    if isinstance(value, int):
        return "Int"
    elif isinstance(value, str):
        return "String"
    elif isinstance(value, float):
        return "Float"
    elif isinstance(value, bool):
        return "Boolean"
    elif isinstance(value, decimal.Decimal):
        return "Decimal"
    elif isinstance(value, datetime.date):
        return "Date"
    elif isinstance(value, datetime.datetime):
        return "DateTime"
    elif isinstance(value, datetime.time):
        return "Time"
    elif isinstance(value, uuid.UUID):
        return "UUID"
    elif value == None:
        return "Void"
    else:
        return "Unknown"


def create_gql_core_setup(list_to_check: list = []):
    queries = {}
    for query in list_to_check:
        q = NestedNamespace(**query)
        queries[q.name] = {}
        for field in q.args:
            setup = Instance(
                default=None
                if field.defaultValue == "null"
                else try_json(field.defaultValue),
                required=(field.type.kind == "NON_NULL"),
                isObject=False,
            )
            if field.type.ofType:
                type_name = field.type.ofType.name
                setup.type = type_name
                inputFields = field.type.ofType.inputFields
                is_object = field.type.ofType.kind == "INPUT_OBJECT"
                setup.isObject = is_object
                if inputFields:
                    items = {}
                    for inputKey in inputFields:
                        defaultValue = try_json(inputKey.defaultValue)
                        type_name = inputKey.type.name
                        if not type_name:
                            type_name = get_scalar_type(defaultValue)
                        setup_fields = Instance(default=defaultValue, type=type_name)
                        items[inputKey.name] = setup_fields.__dict__
                    setup.default = items
            if (
                not setup.default
                and not setup.required
                and not setup.required
                and not setup.type
            ):
                setup.type = "String"
            queries[q.name][field.name] = setup.__dict__
    return queries


def make_gql_query(query_list: list = [], is_mutation: bool = False):
    query_items = []
    for query, fields in query_list.items():
        if is_mutation:
            query_text = f"""mutation {query}"""
        else:
            query_text = f"""query {query}"""
        input_setup = []
        query_setup = []
        is_page = False
        for name, setup in fields.items():
            if not setup.get("isObject"):  # Scalar
                type_name = setup.get("type")
                required = "!" if setup.get("required") else ""
                type_name += required
                if type_name:
                    input_setup.append(f"${name}: {type_name}")
                    query_setup.append(f"{name}: ${name}")

            else:
                input_setup_c = []
                query_setup_c = {name: []}
                for name_c, setup_c in setup.get("default", {}).items():
                    if name.lower() == "pagination":
                        is_page = True
                    type_name = setup_c.get("type")
                    required = "!" if setup_c.get("required") else ""
                    type_name += required
                    if type_name:
                        input_setup_c.append(f"${name_c}: {type_name}")
                        query_setup_c[name].append(f"{name_c}: ${name_c}")
                input_setup.extend(input_setup_c)
                query_setup.append(
                    f"""{name}: {{ {", ".join(query_setup_c[name])} }}"""
                )
        if is_mutation:
            query_output = """
    ... on Error {
        error
        type
        messages
        meta
    }""".strip()
        elif not is_page:
            query_output = "id"
        else:
            query_output = """
    pageInfo {
      pages
    }
    edges {
      node {
        id
      }
    }
    """.strip()

        query_string = f"""{query_text} ({", ".join(input_setup)}) {{\n {query} ({", ".join(query_setup)}) {{ \n {query_output} \n }} \n}}"""
        query_items.append(query_string)
    return "\n\n".join(query_items)


def create_js_forms(all_forms: list = []):
    output = {}
    for schema, fields in all_forms.items():
        output[schema] = {}
        for field, setup in fields.items():
            is_object = setup.get("isObject")
            default_value = setup.get("default")
            if is_object:
                output[schema][field] = {}
                for fkey, fsetup in default_value.items():
                    output[schema][field][fkey] = fsetup.get("default")
            else:
                output[schema][field] = default_value
    return output


def make_gql_setup_core(query: list = [], mutation: list = []):
    setup = {}
    if query:
        setup["query"] = create_gql_core_setup(query)
    if mutation:
        setup["mutation"] = create_gql_core_setup(mutation)
    all_forms = {}
    all_forms.update(setup.get("query", {}))
    all_forms.update(setup.get("mutation", {}))
    actions_example = (
        make_gql_query(setup.get("query", {}))
        + "\n\n"
        + make_gql_query(setup.get("mutation", {}), True)
    )
    return_value = {
        "keys": sorted(list(all_forms.keys())),
        "schema": all_forms,
        "form": create_js_forms(all_forms),
        "code": actions_example,
    }
    return return_value


def js_forms_code(forms):
    code = f"""const FORMS = { forms };"""
    code += "\n\n"
    code += """
class GqlForm {
  constructor(setup) {
    this.$default = () => ({ ...setup });
    this.reset();
  }

  static $create(setup) {
    return new GqlForm(setup);
  }

  reset() {
    this.form = this.$default();
  }
}

function gqlSetup(setup) {
  const output = {};
  Object.keys(setup).forEach((form) => {
    const model = GqlForm.$create(setup[form]);
    output[form] = model;
  });
  return output;
}

const SETUP = gqlSetup(FORMS);
SETUP.$keys = Object.keys(FORMS)

export default SETUP;
""".strip()

    return code


INFO_QUERY = """
fragment InfoIntrospection on __Type {
  return: fields {
    name
    args {
      name
      defaultValue
      type {
        kind
        ofType {
          name
          kind
          inputFields {
            name
            defaultValue
            type {
              name
            }
          }
        }
      }
    }
  }
}

query availableQueries {
  schema: __type(name: "Query") {
    ...InfoIntrospection
  }
}

query availableMutations {
  schema: __type(name: "Mutation") {
    ...InfoIntrospection
  }
}
"""


def build_gql_setup_files(setup):
    roles_dir = BASE_DIR / "roles"
    static_dir = BASE_DIR / "static"

    if setup.get("code"):
        code_text = setup.get("code")
        del setup["code"]

    if setup.get("all_operations"):
        all_operations = setup.get("all_operations")
        del setup["all_operations"]

    with open(str(roles_dir / "actions.graphql"), "w") as file:
        file.write(code_text)
    with open(str(static_dir / "schema.js"), "w") as file:
        file.write(f"""export default { json.dumps(setup, indent=4) }""")
    with open(str(static_dir / "forms.js"), "w") as file:
        code = js_forms_code(json.dumps(setup.get("form"), indent=4))
        file.write(code)
    with open(str(static_dir / "operations.js"), "w") as file:
        file.write(f"""export default { json.dumps(all_operations, indent=4) }""")
    return setup


def gql_schema_info(schema):
    # Core Setup
    queries_resp = schema.execute_sync(INFO_QUERY, operation_name="availableQueries")
    mutations_resp = schema.execute_sync(
        INFO_QUERY, operation_name="availableMutations"
    )
    query = queries_resp.data["schema"]["return"]
    mutation = mutations_resp.data["schema"]["return"]
    setup = make_gql_setup_core(query=query, mutation=mutation)
    # Add Roles
    Role = Roles(schema)
    setup["all_operations"] = Role._all_operations
    build_gql_setup_files(setup)
    return setup
