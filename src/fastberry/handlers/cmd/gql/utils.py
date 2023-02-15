from pathlib import Path
from types import SimpleNamespace
import json

INTROSPECT_OBJECTS = """query IntrospectionQuery{__schema{queryType{name}mutationType{name}subscriptionType{name}types{...FullType}directives{name description locations args{...InputValue}}}}fragment FullType on __Type{kind name description fields(includeDeprecated:true){name description args{...InputValue}type{...TypeRef}isDeprecated deprecationReason}inputFields{...InputValue}interfaces{...TypeRef}enumValues(includeDeprecated:true){name description isDeprecated deprecationReason}possibleTypes{...TypeRef}}fragment InputValue on __InputValue{name description type{...TypeRef}defaultValue}fragment TypeRef on __Type{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name}}}}}}}"""

# schema.execute_sync(INTROSPECT_OBJECTS, variable_values=None)
POSSIBLE_TYPES = {
    "schema": ["queryType", "mutationType", "subscriptionType", "types", "directives"],
    "types": ["OBJECT", "SCALAR", "ENUM", "INPUT_OBJECT", "UNION"],
    "objects": [
        "kind",
        "name",
        "description",
        "fields",
        "inputFields",
        "interfaces",
        "enumValues",
        "possibleTypes",
    ],
}


def graphql_introspect_objects(schema):
    results = schema.execute_sync(INTROSPECT_OBJECTS, variable_values=None)
    return results.data.get("__schema", {})


def get_types(schema):
    out_schema = {}
    for item in schema.get("types", []):
        kind = item.get("kind")
        if out_schema.get(kind):
            out_schema[kind].append(item)
        else:
            out_schema[kind] = []
            out_schema[kind].append(item)
    return out_schema


def transform_field(field):
    if not field.get("required"):
        field["required"] = False
    if not field.get("list"):
        field["list"] = False
    if not field.get("defaultValue"):
        field["defaultValue"] = None
    return field


def get_field_info(field):
    current = SimpleNamespace(**transform_field(field))
    if not current.ofType:
        return current
    else:
        current_dict = get_field_info(current.ofType)
        # Trying to Fix IT
        if current.kind == "NON_NULL":
            current_dict.required = True
        if current.kind == "LIST":
            current_dict.list = True
        return current_dict


def get_object_fields(fields):
    items = {}
    for field in fields:
        field = SimpleNamespace(**field)
        field_kind = field.type.get("kind")
        current_field = get_field_info(field.type)
        current_field = current_field.__dict__
        del current_field["ofType"]
        if "SCALAR" == current_field.get("kind") and field_kind == "NON_NULL":
            current_field["required"] = True
        if field_kind == "LIST":
            current_field["list"] = True
        items[field.name] = current_field
    return items


def get_input_config(all_args):
    field_list = []
    form_dict = {}
    for field in all_args:
        # Step 1
        current = get_field_info(field["type"])
        if field["defaultValue"] in ["null", "None", None]:
            default_value = "null"
        else:
            default_value = field["defaultValue"]
        # Step 2
        try:
            default_value = json.loads(default_value)
        except:
            default_value = None
        # Step 3
        current.defaultValue = default_value
        field_dict = current.__dict__
        del field_dict["ofType"]
        # Append
        form_dict[field["name"]] = field_dict["defaultValue"]
        field_list.append(
            {
                "name": field["name"],
                "type": field_dict,
            }
        )
    return field_list, form_dict


def get_op_args(operations):
    items = {}
    for item in operations:
        field_list, form_dict = get_input_config(item.get("args"))
        items[item.get("name")] = {
            "args": field_list,
            "form": form_dict,
        }
    return items


def get_graphql_objects_base(graphql_objects):
    all_graphql_objects = {}
    for item in graphql_objects:
        name = item.get("name")
        fields = item.get("fields")
        if not name.startswith("__") and name not in ["Query", "Mutation"]:
            current_config = get_object_fields(fields)
            for key, conf in current_config.items():
                del conf["defaultValue"]
            all_graphql_objects[name] = current_config
        elif name in ["Query", "Mutation"]:
            obj_types = get_object_fields(fields)
            obj_args = get_op_args(fields)
            all_graphql_objects[name] = {}
            for key, val in obj_types.items():
                all_graphql_objects[name][key] = {"type": val, **obj_args[key]}
    return all_graphql_objects


def get_graphql_objects(all_objects):
    all_objs = get_graphql_objects_base(all_objects)
    all_query = all_objs.get("Query")
    all_mutation = all_objs.get("Mutation")
    if all_query:
        del all_objs["Query"]
    if all_mutation:
        del all_objs["Mutation"]
    return {
        "OBJECT": all_objs,
        "Query": all_query,
        "Mutation": all_mutation,
    }


def get_graphql_input_objects(graphql_input_objects):
    dict_out = {}
    for item in graphql_input_objects:
        field_list, form_dict = get_input_config(item["inputFields"])
        # Dict Inject
        dict_out[item["name"]] = {
            "args": field_list,
            "form": form_dict,
        }
    return dict_out


def get_graphql_scalars(graphql_scalars):
    all_graphql_scalars = set()
    for item in graphql_scalars:
        all_graphql_scalars.add(item.get("name"))
    return list(all_graphql_scalars)


def get_graphql_unions(graphql_unions):
    all_graphql_unions = {}
    for item in graphql_unions:
        item = SimpleNamespace(**item)
        all_graphql_unions[item.name] = {}
        for gtype in item.possibleTypes:
            current = transform_field(
                {
                    "kind": gtype.get("kind"),
                    "name": gtype.get("name"),
                }
            )
            del current["defaultValue"]
            all_graphql_unions[item.name][gtype.get("name")] = current
    return all_graphql_unions


def get_graphql_enum(all_enum):
    all_graphql_enum = {}
    for item in all_enum:
        name = item.get("name")
        if not name.startswith("__"):
            all_graphql_enum[name] = [val.get("name") for val in item.get("enumValues")]
    return all_graphql_enum


def transform_operations(schema, current):
    current_type = current["type"]
    current_form = current["form"]
    current_args = current["args"]
    for field in current_args:
        if field["type"]["kind"] == "INPUT_OBJECT":
            input_form = (
                schema["INPUT_OBJECT"].get(field["type"]["name"], {}).get("form")
            )
            current_form[field["name"]] = input_form
    return {"type": current_type, "args": current_args, "form": current_form}


def get_all_transform_operations(schema, op_type):
    query_ops = {}
    all_query = schema.get(op_type, {})
    for op in all_query.keys():
        current = all_query.get(op)
        query_ops[op] = transform_operations(schema, current)
    return query_ops


def parse_graphql_schema(schema, include_input_object=True):
    # Step 1
    schema_introspect = graphql_introspect_objects(schema)
    schema_types = get_types(schema_introspect)
    return_object = get_graphql_objects(schema_types["OBJECT"])
    # Step 2
    schema_dict = {
        **return_object,
        "UNION": get_graphql_unions(schema_types.get("UNION")),
        "SCALAR": get_graphql_scalars(schema_types.get("SCALAR")),
        "INPUT_OBJECT": get_graphql_input_objects(schema_types.get("INPUT_OBJECT")),
        "ENUM": get_graphql_enum(schema_types.get("ENUM")),
    }
    # Step 3
    schema_dict["Query"] = get_all_transform_operations(schema_dict, "Query")
    schema_dict["Mutation"] = get_all_transform_operations(schema_dict, "Mutation")
    # Step 4
    if not include_input_object:
        del schema_dict["INPUT_OBJECT"]
    # Schema Out
    return schema_dict


def write_file(path, data):
    file_path = Path(path)
    parent_dir = file_path.parent
    if not parent_dir.exists():
        parent_dir.mkdir(parents=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(data)


def create_frontend_objects(all_objs):
    frontend_setup = {}
    for name, config in all_objs.items():
        config_js = {}
        for field_name, field_config in config.items():
            match field_config["kind"]:
                case "SCALAR":
                    config_js[field_name] = True
                case "OBJECT":
                    # "#" +
                    config_js[field_name] = field_config["name"]
        frontend_setup[name] = config_js

    return frontend_setup


def create_frontend_operations(schema, all_objs):
    query_frontend = {}
    for name, config in all_objs.items():
        return_value = None
        match config["type"]["kind"]:
            case "SCALAR":
                return_value = None
            case "OBJECT":
                return_value = [config["type"]["name"]]
            case "UNION":
                child_name = config["type"]["name"]
                return_value = list(schema["UNION"][child_name].keys())
        query_frontend[name] = {
            "model": return_value,
            "args": config["args"],
            "form": config["form"],
        }
    return query_frontend


class Frontend:
    def __init__(self, schema):
        self._schema = parse_graphql_schema(schema, True)

    @property
    def query(self):
        items = self._schema.get("Query")
        if items:
            return create_frontend_operations(self._schema, items)
        return {}

    @property
    def mutation(self):
        items = self._schema.get("Mutation")
        if items:
            return create_frontend_operations(self._schema, items)
        return {}

    @property
    def models(self):
        items = self._schema.get("OBJECT")
        if items:
            schema = create_frontend_objects(items)
            return json.dumps(schema, indent=4)
        return {}

    @property
    def schema(self):
        return json.dumps(
            {
                "query": self.query,
                "mutation": self.mutation,
                "enum": self._schema.get("ENUM"),
                "scalar": self._schema.get("SCALAR"),
                "forms": self._schema.get("INPUT_OBJECT"),
            },
            indent=0,
        )
