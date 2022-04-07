"""
    Run FastAPI Server
"""

import json

import click

from ... import Settings
from .shell import shell_commands, shell_print

settings = Settings()


@click.command()
@click.option(
    "-m",
    "--mode",
    type=click.Choice(["development", "staging", "production"]),
    default="development",
    help="Server Mode.",
)
@click.option("-p", "--port", default=8000, help="Port Number.")
@click.option("-w", "--workers", default=1, help="Number of Workers.")
def run(mode, port, workers):
    """Start FastApi Server

    \b
    # Examples
        - development : ./manage.py run --port 8000 --mode development
        - staging     : ./manage.py run --port 8000 --mode staging
        - production  : ./manage.py run --port 8000 --mode production --workers 4
    """

    # SETUP
    return_value = []

    # Get Path(s)
    base_dir = settings.base_dir
    conf_dir = base_dir / "config"

    # Create Path(s)
    conf_dir.mkdir(parents=True, exist_ok=True)

    # Write Mode <File>
    click.secho("")
    with open(conf_dir / "mode.json", "w", encoding="utf-8") as file:
        shell_print(
            f"* Writing to ./config/mode.json ... { json.dumps(dict(mode=mode)) }"
        )
        mode_json = json.dumps(dict(mode=mode), indent=4)
        file.write(mode_json)

    # PY-Lint
    if mode == "development":
        return_value.append("""python scripts/pylint.py > logs/pylint.log 2>&1 &""")

    # FastAPI-Server
    match mode:
        case "development":
            run_server = f"python -m uvicorn main:app --reload --port { port }"
        case "staging":
            run_server = f"python -m uvicorn main:app --reload --port { port }"
        case "production":
            run_server = f"python -m gunicorn main:app --workers { workers } --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:{ port }"
                    
    return_value.append(run_server)

    # Message
    shell_print(f"* Starting FastApi Server... (Mode: { mode })\n")

    # RETURN-VALUE
    shell_commands(return_value)
