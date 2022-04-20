"""
Project Settings
"""

import pathlib

from fastberry import Fastberry

BASE_DIR = pathlib.Path(__file__).resolve().parents[1]

settings = Fastberry(base_dir=BASE_DIR)
