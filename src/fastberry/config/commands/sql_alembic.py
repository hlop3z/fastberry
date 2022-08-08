"""
    SQLAlchemy + Alembic
"""

import click
import shutil
import os

try:
    from alembic import command
    from alembic.config import Config

    ALEMBIC_CONFIG = Config("alembic.ini")

except ImportError:
    ALEMBIC_CONFIG = None


@click.group()
def cli():
    """Click (CLI) Group"""


@cli.command()
@click.option("-m", "--message", help="Migration message.", type=str, default=None)
def db_migrate(message):
    """Database Make-Migrations & Migrate."""
    # Make-Migrations
    command.revision(ALEMBIC_CONFIG, message=message, autogenerate=True)
    # Migrate
    command.upgrade(ALEMBIC_CONFIG, "head")


@cli.command()
@click.option("-r", "--revision", help="Revision ID.", type=str)
def db_upgrade(revision):
    """Database Migrate (Upgrade)."""
    command.upgrade(ALEMBIC_CONFIG, revision)


@cli.command()
@click.option("-r", "--revision", help="Revision ID.", type=str)
def db_downgrade(revision):
    """Database Migrate (Downgrade)."""
    command.downgrade(ALEMBIC_CONFIG, revision)


@cli.command()
def db_history():
    """Database Migrations History."""
    command.history(ALEMBIC_CONFIG)
    
    
@cli.command()
def db_reset():
    """Database Delete Migrations (All-Versions)."""
    dir_path = "./migrations/versions"
    # Delete
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))
    # Recreate
    os.makedirs(dir_path)
