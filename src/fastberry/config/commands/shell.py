"""
    Shell Functions
"""

import pathlib
import shlex
import shutil
import subprocess
import zipfile

import click

TEMPORARY_DIR = pathlib.Path(__file__).parents[0] / "tmp"


def shell_commands(list_of_commands):
    """Shell Commands"""
    processes = []
    for cmd in list_of_commands:
        __code = shlex.split(cmd)
        task = subprocess.Popen(__code, shell=True)
        processes.append(task)
    return [process.wait() for process in processes]


def shell_print(text: str, color: str = "green"):
    """Shell Print"""
    return click.secho(f"{ text }", fg=color, bold=True)


def path_delete(dir_path):
    """Delete Path"""
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"Error: {dir_path} : {e.strerror}")


def unzip_base(source, destination):
    """Unzip Base"""
    with zipfile.ZipFile(source, "r") as zip_ref:
        zip_ref.extractall(destination)


def unzip(source: str, destination: str):
    """Unzip Method"""
    file_name = source.name
    file_name = file_name.replace(".zip", "")
    unzip_base(source, TEMPORARY_DIR)
    shutil.move(TEMPORARY_DIR / file_name, destination)
