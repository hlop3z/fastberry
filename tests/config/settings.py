# -*- coding: utf-8 -*-
"""
    { Settings }
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
INSTALLED_APPS = ["todo"]

# Database(s)
DATABASES = {
    "sql": {"default": "sqlite:///example.db"}, 
    "mongo": {"default": None},
}