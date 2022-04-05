"""
    Project Core Definitions (aka: Folders & Files)
"""

import json
import types

import yaml

from .settings_base import Settings

FILE_YAML = "settings.yaml"
FILE_MODE = "config/mode.json"
FILE_DOCS = "config/docs.md"
LOAD_ENVS = lambda mode: f"config/env/{ mode }.env"
FILE_ENVS = "config/env/development.env"

SETTING_YAML_QUERYING = {"items_per_page": 50}
SETTING_YAML = {
    "version": "0.0.1",
    "app_name": "FastAPI",
    "admin_email": None,
    "installed_apps": [],
    "development_apps": [],
    "querying": {},
    "allowed_hosts": [],
    "permissions": [],
    "middleware": [],
    "generates": "graphql",
}


def load_yaml():
    """Load <Yaml> File"""
    return_value = None
    with open(FILE_YAML, "r", encoding="utf-8") as stream:
        try:
            settings_yaml = yaml.safe_load(stream)
            settings_dir = {name.lower(): conf for name, conf in settings_yaml.items()}
            # Other Dicts
            SETTING_YAML_QUERYING.update(settings_dir.get("querying", {}))
            settings_dir.update({"querying": SETTING_YAML_QUERYING})
            SETTING_YAML.update(settings_dir)
            return_value = types.SimpleNamespace(**SETTING_YAML)
        except yaml.YAMLError as error:
            print(error)
    return return_value


def load_mode():
    """Load <Yaml> File"""
    return_value = {}
    with open(FILE_MODE, "r", encoding="utf-8") as file:
        try:
            data = file.read()
            if data:
                return_value = json.loads(data)
        except yaml.YAMLError as error:
            print(error)
    return return_value


def load_env(mode: str = None):
    """Load <Dot.Env> File"""
    active_env = LOAD_ENVS(mode) if mode else FILE_ENVS
    return Settings(_env_file=active_env)


def load_docs():
    """Load <Docs> File"""
    DOCS = ""
    with open(FILE_DOCS, "r", encoding="utf-8") as file:
        DOCS = file.read()
    return DOCS
