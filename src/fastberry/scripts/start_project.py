import pathlib
import os

import click

from .shell import unzip, shell_print

TEMPLATES_DIR = pathlib.Path(__file__).parents[0] / "templates"

@click.command()
def cli():
    """Example Script."""
    
    shell_print("""* Starting-Project!""")            
    unzip(TEMPLATES_DIR / "project-template.zip", os.getcwd())