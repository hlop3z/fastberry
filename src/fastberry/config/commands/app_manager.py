"""
    Create A New App
"""

import os.path
import pathlib

import click

from ... import Settings
from .shell import shell_print, unzip

TEMPLATES_DIR = pathlib.Path(__file__).parents[0] / "templates"

settings = Settings()


@click.command()
@click.argument(
    "app_name",
    type=str,
    nargs=1,
)
def start_app(app_name):
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
        unzip(TEMPLATES_DIR / "base_app.zip", the_dir)
