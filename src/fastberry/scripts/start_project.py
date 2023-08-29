"""
    Start A New Fastberry Project
"""

import os
import pathlib

import click

from .shell import unzip, shell_print

TEMPLATES_DIR = pathlib.Path(__file__).parents[0] / "templates"


@click.command()
def cli():
    """Fastberry Start-Project."""

    shell_print("""* Starting-Project! ...\n""")
    unzip(TEMPLATES_DIR / "project-template.zip", pathlib.Path(os.getcwd()))
