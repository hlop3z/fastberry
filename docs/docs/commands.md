> Your code **needs** to be in a **file** named **`commands.py`** or **folder** named **`commands`** inside your **Application**.

> Your **`click.group`** **needs** to be named **`cli`**.

## File or Folder **Layout**

=== ":material-file: File"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- commands.py          --> <File> - Your code in HERE!
    |
    `-- etc...
    ```

=== ":material-folder: Folder"

    ``` text
    root/
    |
    |--  apps/
    |    `--  MY_APP/
    |         `-- commands/           --> <Directory> - Your Commands in HERE!
    |             |-- __init__.py     --> <File> - Your IMPORTS in HERE!
    |             `-- etc...
    |
    `-- etc...
    ```

## Python **Code**

=== ":material-file: File"

    ```python title="commands.py"
    # -*- coding: utf-8 -*-
    """
        Custom - Command-Line-Group
    """

    import click


    # Init Group
    @click.group()
    def cli():
        """Click (CLI) Group"""

    # Create <Commands> here.
    @cli.command()
    def hello_world():
        """Demo CLI Function"""

        print("Hello World")
    ```

=== ":material-folder: Folder"

    ```python title="__init__.py"
    # -*- coding: utf-8 -*-
    """
        Custom - Command-Line-Group
    """

    import click

    # Import <Commands> Here
    from .hello_world import hello_world


    # Init Group
    @click.group()
    def cli():
        """Click (CLI) Group"""


    # Register <Commands> Here
    cli.add_command(hello_world)
    ```

    ```python title="hello_world.py"
    # -*- coding: utf-8 -*-
    """
        Command - Hello World
    """

    import click


    # Create <Commands> here.
    @click.command()
    def hello_world():
        """Demo CLI Function"""

        print("Hello World")

    ```
