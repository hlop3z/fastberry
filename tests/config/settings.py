# -*- coding: utf-8 -*-
""" [Settings]
    Project Settings { app.settings }.
"""
import pathlib

# Base Directory
BASE_DIR = pathlib.Path(__file__).parents[1]

# Installed Apps
# INSTALLED_APPS = ["good_app", "demo"]
INSTALLED_APPS = ["shop"]

SQL_URL = "sqlite:///example.db"
MONGO_URL = "mongodb://localhost:27017/test_database"
