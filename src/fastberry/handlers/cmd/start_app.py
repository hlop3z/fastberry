"""
    Create A New App
"""

import os.path

import click
import spoc

from .action.plugin_maker import create_plugin
from .shell import shell_print, unzip


@click.command()
@click.argument(
    "app_name",
    type=str,
    nargs=1,
)
# @click.option("--gql/--no-gql", default=False, type=bool, help="Init with sample code.")
@click.option(
    "--plugin/--no-plugin", default=False, type=bool, help="Init <App> as a plugin."
)
def start_app(app_name, plugin):
    """Creates a Fastberry App Directory."""
    # Get Path(s)
    apps_dir = spoc.base_dir / "apps"
    the_dir = apps_dir / app_name

    # Create Path(s)
    apps_dir.mkdir(parents=True, exist_ok=True)

    # Check Path(s)
    if os.path.isdir(the_dir):
        shell_print(
            f"""* Error: "{{ { app_name } }}" App Already Exists!""", color="red"
        )
    else:
        shell_print(
            f"""* Starting App: "{{ { app_name } }}" . . .""",
        )
        if plugin:
            the_dir.mkdir(parents=True, exist_ok=True)
            create_plugin(the_dir)
        else:
            unzip("base_app.zip", the_dir)
