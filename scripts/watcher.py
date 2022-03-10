#!/usr/bin/env python

"""Project --> Watchdog:
    This module is to watch for changes in your Python-Project.
    It uses ( isort, black & pylint ) to clean and analyze your <code>.
"""

import subprocess
import time
from pathlib import Path

import watchdog.events
import watchdog.observers


def shell_cmd(name=None, cmd=None, check=True):
    """
    Shell-Command Wrapper
    """
    print(f"""Running... < {name} >""")
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError:
        print(f"""Error while running {name}""")


class Handler(watchdog.events.PatternMatchingEventHandler):
    """Watchdog - Event Handler

    Note:
        EVENT_OPTIONS: on_created, on_modified, on_deleted, on_moved, on_any_event

    Methods:
        event_name(self, event): Do something < After > the event happens.

    Example:
        def on_modified(self, event):
            path_to_watch = event.src_path
            # After Event - Do Something ...
    """

    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(
            self,
            patterns=["*.py"],  # File Types
            ignore_directories=True,
            case_sensitive=False,
        )

    def on_modified(self, event):
        path_to_watch = event.src_path
        print(f"""Fixing... { path_to_watch }""")

        # After Event - Do Something ...
        shell_cmd("isort", f'''python -m isort --profile black "{ path_to_watch }"''')
        shell_cmd("black", f'''python -m black "{ path_to_watch }"''')
        shell_cmd("pylint", f'''python -m pylint "{ path_to_watch }"''', check=False)


# -----------------------------------------------------------------------------
# < Script > - Run
# -----------------------------------------------------------------------------
def main():
    """Dexter-Watch

    Watch over your project as you write it and ensure you follow code-style (black & isort).
    Also, it rates your code with (pylint).
    """

    # Base Directory
    base_dir = Path(__file__).parents[1]

    # Watchdog Handler
    event_handler = Handler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path=base_dir, recursive=True)
    observer.start()

    # Run "Server"
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
