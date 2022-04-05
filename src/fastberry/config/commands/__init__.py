"""
    Fastberry Command-Line-Interface
"""

import click

# Import Commands Here
from .app_manager import start_app
from .graphql import graphql
from .run import run


@click.group()
def cli():
    """Click (CLI) Group"""


# Add Commands Here
cli.add_command(run)
cli.add_command(graphql)
cli.add_command(start_app)
