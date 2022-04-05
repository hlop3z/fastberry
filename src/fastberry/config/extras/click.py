"""Click (CLI) Util

methods:
    command_collection: Create <click> Command-Line-Interface by grouping all commands.
    is_crud: Check if value is a subclass ot <CRUD>.
"""

import click

TITLE = "Fastberry"

HELP_TEXT = f"""
Welcome to { TITLE }
"""


def is_click(module):
    """Check if is <click>"""
    return isinstance(module, click.core.Group)


def command_collection(sources: list):
    """Create <click> Command-Line-Interface"""
    sources = sources or []
    return click.CommandCollection(name=TITLE, help=HELP_TEXT, sources=sources)
