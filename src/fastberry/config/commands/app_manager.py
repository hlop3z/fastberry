"""
    Create A New App
"""

import os.path
import pathlib

import click

from ... import Settings
from .plugin_maker import create_plugin
from .shell import shell_print, unzip

TEMPLATES_DIR = pathlib.Path(__file__).parents[0] / "templates"

settings = Settings()


@click.command()
@click.argument(
    "app_name",
    type=str,
    nargs=1,
)
@click.option(
    "--demo/--no-demo", default=False, type=bool, help="Init with sample code."
)
@click.option(
    "--plugin/--no-plugin", default=False, type=bool, help="Init <App> as a plugin."
)
def start_app(app_name, demo, plugin):
    """Creates a Fastberry App Directory."""

    # Get Path(s)
    apps_dir = settings.base_dir / "apps"
    the_dir = apps_dir / app_name

    # Create Path(s)
    apps_dir.mkdir(parents=True, exist_ok=True)

    # Check Path(s)
    if os.path.isdir(the_dir):
        shell_print(f"""* App: "{ app_name }" Already Exists!""", color="red")
    else:
        shell_print(
            f"""* Starting App: "{ app_name }" ...""",
        )
        if demo:
            unzip(TEMPLATES_DIR / "base_app.zip", the_dir)
        else:
            the_dir.mkdir(parents=True, exist_ok=True)
            if plugin:
                create_plugin(the_dir)
