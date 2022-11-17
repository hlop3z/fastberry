# -*- coding: utf-8 -*-
"""
    { Settings }
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = []

# SQL & Mongo - Databases
DATABASES = {
    "sql": {"default": None},  # Example: sqlite:///example.db
    "mongo": {"default": None},  # Example: mongodb://localhost:27017/example
}
