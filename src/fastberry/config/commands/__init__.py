"""
    Fastberry Command-Line-Interface
"""

import click

# Import Commands Here
from .app_manager import start_app
from .graphql import graphql
from .run import run
from .sql_alembic import cli as cli_sql


@click.group()
def cli_basics():
    """Click (CLI) Group"""


# Add Commands Here
cli_basics.add_command(run)
cli_basics.add_command(graphql)
cli_basics.add_command(start_app)


cli = click.CommandCollection(sources=[cli_sql, cli_basics])
