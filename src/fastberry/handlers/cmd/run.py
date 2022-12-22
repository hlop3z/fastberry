"""
    Run the API
"""
import click
import spoc
import os

from .shell import shell_print


@click.command()
@click.option("-p", "--port", default=8000, help="Port Number.")
@click.option("-w", "--workers", default=1, help="Number of Workers.")
def run(port, workers):
    """Start { FastBerry } Server

    \b
    # Examples
        - development          : `./manage.py run --port 8000`
        - production & staging : `./manage.py run --port 8000 --workers 4`
    """
    mode = spoc.mode
    host = "0.0.0.0"
    # FastAPI-Server
    match mode:
        case "development":
            cmd = f"python -m uvicorn main:app --reload --port { port } --host { host }"
        case "staging":
            cmd = f"python -m gunicorn main:app --workers { workers } --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:{ port }"
        case "production":
            cmd = f"python -m gunicorn main:app --workers { workers } --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:{ port }"

    # Message
    shell_print(f"* Starting FastApi Server... (Mode: { mode.title() })\n")

    # RETURN-VALUE
    os.system(cmd)
