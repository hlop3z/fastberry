# -*- coding: utf-8 -*-
"""
    { Settings }
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS: list = []

# Database(s)
DATABASES = {
    "sql": {"default": None},  # Example: sqlite:///example.db
    "mongo": {"default": None},  # Example: mongodb://localhost:27017/example
}
