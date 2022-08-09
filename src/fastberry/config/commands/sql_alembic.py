"""
    SQLAlchemy + Alembic
"""

import os
import shutil
import pathlib
import click

try:
    from alembic import command
    from alembic.config import Config

    ALEMBIC_CONFIG = Config("alembic.ini")

except ImportError:
    ALEMBIC_CONFIG = None


@click.group()
def db():
    """Database Migrations Commands"""


@db.command()
@click.option("-m", "--message", help="Migration message.", type=str, default=None)
def make_migrations(message):
    """Database Make-Migrations."""
    command.revision(ALEMBIC_CONFIG, message=message, autogenerate=True)


@db.command()
def migrate():
    """Database Migrate."""
    command.upgrade(ALEMBIC_CONFIG, "head")


@db.command()
@click.option("-m", "--message", help="Migration message.", type=str, default=None)
def auto_migrate(message):
    """Database Make-Migrations & Migrate."""
    # Make-Migrations
    command.revision(ALEMBIC_CONFIG, message=message, autogenerate=True)
    # Migrate
    command.upgrade(ALEMBIC_CONFIG, "head")


@db.command()
@click.option("-r", "--revision", help="Revision ID.", type=str)
def upgrade(revision):
    """Database Migrate (Upgrade)."""
    command.upgrade(ALEMBIC_CONFIG, revision)


@db.command()
@click.option("-r", "--revision", help="Revision ID.", type=str)
def downgrade(revision):
    """Database Migrate (Downgrade)."""
    command.downgrade(ALEMBIC_CONFIG, revision)


@db.command()
def history():
    """Database Migrations History."""
    command.history(ALEMBIC_CONFIG)


@db.command()
def reset():
    """Database Delete Migrations (All-Versions)."""
    dir_path = pathlib.Path("./migrations/versions")
    # Delete
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")
    # Recreate
    os.makedirs(dir_path)
    with open(dir_path / "README", "w") as f:
        f.write("Database Migrations Versions")
