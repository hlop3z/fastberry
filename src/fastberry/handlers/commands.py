"""
    Commands
"""
import click

from .cmd import cli

TITLE = "Fastberry"

HELP_TEXT = f"""
Welcome to { TITLE }
"""


def commands(commands: list):
    """Collect (Click) Commands"""
    command_sources = [cli]
    for active in commands:
        if isinstance(active.object, click.core.Group):
            command_sources.append(active.object)
    return click.CommandCollection(name=TITLE, help=HELP_TEXT, sources=command_sources)
