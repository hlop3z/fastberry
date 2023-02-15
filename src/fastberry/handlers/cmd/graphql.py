"""
    GraphQL (Schema + Operations)
"""

import datetime
import decimal
import functools
import json
import os
import shutil

import click

from ...tools import to_camel_case
from .gql import build_client, introspection_info
from .shell import shell_print, unzip, zip


def get_controller():
    """Get Controller"""
    from ... import App

    return App()


SCALAR_INPUT = {
    list: "Array",
    str: "String",
    int: "Integer",
    float: "Float",
    bool: "Boolean",
    decimal.Decimal: "Decimal",
    datetime.date: "Date",
    datetime.datetime: "Datetime",
    datetime.time: "Time",
}


def reset_folder(folder):
    """Reset Folder"""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def create_graphql_types(types):
    """Get All Custom-Types"""

    setup = {}
    for model in types:
        class_name = model.__name__
        fields = model.__spoc__.config["annotations"]
        setup[class_name] = {"id": True}
        for key, val in fields.items():
            camel_key = to_camel_case(key)
            if val.scalar:
                setup[class_name][camel_key] = True
            else:
                try:
                    forward_name = val.real.__forward_arg__
                except:
                    forward_name = val.real
                setup[class_name][camel_key] = forward_name
    return setup


def form_default_value(value, input_type):
    """Form: Get Default Value"""
    output = None
    if input_type == "string":
        output = ""
    elif value == list:
        output = []
    return output


def create_graphql_forms(forms):
    """Get All Custom-Forms"""

    setup = {}
    for cls in forms:
        annotations = cls.__spoc__.config["annotations"]
        name = cls.__name__
        setup[name] = {
            "name": name,
            "fields": [],
            "labels": {},
            "form": {},
        }
        for key, val in annotations.items():
            camel_key = to_camel_case(key)
            input_type = SCALAR_INPUT.get(val)
            input_type = input_type or "string"
            value = form_default_value(val, input_type)
            field = {
                "name": camel_key,
                "type": input_type,
            }
            setup[name]["fields"].append(field)
            setup[name]["labels"][camel_key] = key.title().replace("_", " ")
            setup[name]["form"][camel_key] = value

    return setup


def pretty(items):
    """Pretty (Operations)"""
    return sorted(list(set(items)))


def clean_print_name(base_dir, active):
    """Clean Print Name"""
    return os.path.relpath(active, base_dir)


def write_json(path, data, javascript=False):
    """Write JSON File"""
    with open(path, "w", encoding="utf-8") as file:
        json_data = json.dumps(data, indent=4, sort_keys=True)
        if javascript:
            json_data = f"export default {json_data}"
        file.write(json_data)


def write_schema(path, data):
    """Write Schema File"""
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(data))


def go_to_path(base_dir, user_dir, default_dir="graphql"):
    """Go To Path By String"""
    out_dir = base_dir
    if user_dir == "" or not user_dir:
        user_dir = default_dir
    for path in user_dir.split("/"):
        out_dir = out_dir / path
    return out_dir


@click.command(name="schema")
@click.option(
    "-c",
    "--client",
    default=False,
    is_flag=True,
    show_default=True,
    help="Create JavaScript GraphQL.",
)
def graphql(client):
    """Build GraphQL (Schema + Operations)"""
    controller = get_controller()

    # Settings Path(s)
    generates_dir = controller.core.config["spoc"].get("spoc", {}).get("generates")

    # Get Path(s)
    base_dir = controller.core.base_dir
    output_dir = go_to_path(base_dir, generates_dir, "graphql")

    # Create Path(s)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clean
    reset_folder(output_dir)

    # Output Paths <Files>
    codeout = {
        "schema": output_dir / "schema.graphql",
        "schema-ops": output_dir / "operations.json",
    }

    clean_name = functools.partial(clean_print_name, output_dir)

    # Core Information
    messages = {
        "main-folder": "[Building]: Schema & Operations . . .",
        "folder": f"[Folder]: {output_dir}",
    }

    size = len(messages["folder"])
    messages["cool-folder"] = "-" * size

    # GraphQL (Schema)
    schema = controller.graphql.schema()
    schema_info = introspection_info(schema)

    # Names (Operations)
    # query_names = controller.graphql.info.query
    # mutation_names = controller.graphql.info.mutation
    # query_names_camel = set()
    # mutation_names_camel = set()

    # for x in query_names:
    #     query_names_camel.add(to_camel_case(x))
    # for x in mutation_names:
    #     mutation_names_camel.add(to_camel_case(x))

    # operations_names = {
    #     "query": pretty(query_names_camel),
    #     "mutation": pretty(mutation_names_camel),
    # }

    if client:
        # Fastberry GraphQL
        shell_print(messages["cool-folder"])
        shell_print("[FastBerry]: Creating GraphQL Client...")
        shell_print(messages["cool-folder"])
        shell_print(messages["folder"])
        shell_print(messages["cool-folder"])
        shell_print(
            """* [Folder] : client/""",
            color="yellow",
        )
        shell_print(
            """* [ReadMe] : README.md """,
            color="yellow",
        )
        build_client(schema)
    else:
        # Core GraphQL
        shell_print(messages["cool-folder"])
        shell_print(messages["main-folder"])
        shell_print(messages["cool-folder"])
        shell_print(messages["folder"])
        shell_print(messages["cool-folder"])
        shell_print(
            f"""* [Schema]         : { clean_name(codeout["schema"]) }""",
            color="yellow",
        )
        shell_print(
            f"""* [Operations]     : { clean_name(codeout["schema-ops"]) }""",
            color="yellow",
        )
        # Outputs
        write_schema(codeout["schema"], schema)
        write_json(codeout["schema-ops"], schema_info)
