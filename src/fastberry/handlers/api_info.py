# -*- coding: utf-8 -*-
"""
    Main Settings Required For The API
"""
import typing

from ..core import types


def api_info(
    base_dir: typing.Any = None, pyproject: typing.Any = None, toml: typing.Any = None
):
    """API's Info"""
    current_path = base_dir
    current_info = pyproject.get("project", {})
    # Get { Docs }
    app_description = None
    docs_file = toml.get("spoc", {}).get("docs")
    if docs_file:
        for path in docs_file.split("/"):
            current_path /= path
        if current_path.exists():
            with open(current_path, "r", encoding="utf-8") as file:
                app_description = file.read()
    # FastAPI { INFO }
    return types.FastAPI(
        title=current_info.get("name", "fastberry"),
        version=current_info.get("version", "0.1.0"),
        description=app_description,
    )
