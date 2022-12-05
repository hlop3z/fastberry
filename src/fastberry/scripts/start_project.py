"""
    Start A New Fastberry Project
"""

import os
import pathlib

import click

from ..handlers.cmd.shell import shell_print
from .shell import unzip

TEMPLATES_DIR = pathlib.Path(__file__).parents[0] / "templates"


@click.command()
def cli():
    """Fastberry Start-Project."""

    shell_print("""* Starting-Project! ...\n""")
    unzip(TEMPLATES_DIR / "project-template.zip", pathlib.Path(os.getcwd()))
