"""
    GraphQL (Schema + Operations)
"""

import json
import os.path

import click

from ... import Schema, Fastberry

settings = Fastberry()


def to_camel_case(text):
    """Converts to Camel-Case"""
    init, *temp = text.split("_")
    return "".join([init.lower(), *map(str.title, temp)])


def read_files(root_path):
    """Read All .graphql Files"""
    outputs = []
    if os.path.isdir(root_path):
        for item in root_path.glob("**/*.graphql"):
            with open(item, "r", encoding="utf-8") as file:
                code = file.read()
                outputs.append(code)
    return outputs


def get_operations(base_dir):
    """Get App GraphQL Operations"""
    # Operations <Files>
    operations_location = base_dir / "operations"
    operations_core = operations_location / "core"
    operations_desktop = operations_location / "desktop"
    operations_mobile = operations_location / "mobile"

    # Return Values
    outputs = dict(core=[], desktop=[], mobile=[])
    outputs["core"].extend(read_files(operations_core))
    outputs["desktop"].extend(read_files(operations_desktop))
    outputs["mobile"].extend(read_files(operations_mobile))

    # Return
    return outputs


def shell_print(text: str, color: str = "green"):
    """Customized Click Echo"""
    return click.secho(f"{ text }", fg=color, bold=True)


@click.command(name="schema")
def graphql():
    """Build GraphQL (Schema + Operations)"""

    # Get Path(s)
    output_dir = settings.base_dir
    generates_file = settings.base.generates
    if generates_file == "" or not generates_file:
        generates_file = "graphql"
    for path in generates_file.split("/"):
        output_dir = output_dir / path

    # Create Path(s)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output Paths <Files>
    core_operations = output_dir / "core.graphql"
    desktop_operations = output_dir / "desktop.graphql"
    mobile_operations = output_dir / "mobile.graphql"
    schema_graphql = output_dir / "schema.graphql"
    schema_json = output_dir / "operations.json"

    # Outputs
    shell_print("* Collecting All Operations From...", color="magenta")
    shell_print("\t * <app_name>/operations/core...", color="magenta")
    shell_print("\t * <app_name>/operations/desktop...", color="magenta")
    shell_print("\t * <app_name>/operations/mobile... \n", color="magenta")
    outputs = dict(core=[], desktop=[], mobile=[])
    for path in settings.apps.paths:
        code = get_operations(path)
        outputs["core"].extend(code["core"])
        outputs["desktop"].extend(code["desktop"])
        outputs["mobile"].extend(code["mobile"])

    # Finally
    core = "\n\n".join(outputs["core"])
    desktop = "\n\n".join(outputs["desktop"])
    mobile = "\n\n".join(outputs["mobile"])

    shell_print("* Building Schema & Operations ...")
    shell_print(f"\t * [schema]     : { schema_graphql }")
    shell_print(f"\t * [core]       : { core_operations }")
    shell_print(f"\t * [desktop]    : { desktop_operations }")
    shell_print(f"\t * [mobile]     : { mobile_operations }")
    shell_print(f"\t * [operations] : { schema_json }")

    # Core (Operations)
    with open(core_operations, "w", encoding="utf-8") as file:
        file.write(core)

    # Desktop (Operations)
    with open(desktop_operations, "w", encoding="utf-8") as file:
        file.write(desktop)

    # Mobile (Operations)
    with open(mobile_operations, "w", encoding="utf-8") as file:
        file.write(mobile)

    # GraphQL (Schema)
    schema = Schema(
        query=settings.apps.schema.Query,
        mutation=settings.apps.schema.Mutation,
    )
    with open(schema_graphql, "w", encoding="utf-8") as file:
        file.write(str(schema))

    # Names (Operations)
    query_names = settings.apps.operations.query
    mutation_names = settings.apps.operations.mutation
    query_names_camel = set()
    mutation_names_camel = set()

    for x in query_names:
        query_names_camel.add(to_camel_case(x))
    for x in mutation_names:
        mutation_names_camel.add(to_camel_case(x))

    # Pretty (Operations)
    pretty = lambda items: sorted(list(set(items)))
    operations_names = dict(
        python=dict(query=pretty(query_names), mutation=pretty(mutation_names)),
        graphql=dict(
            query=pretty(query_names_camel), mutation=pretty(mutation_names_camel)
        ),
    )

    # Output (Operations)
    with open(schema_json, "w", encoding="utf-8") as file:
        file.write(json.dumps(operations_names, indent=4))
