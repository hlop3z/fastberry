"""
Project Settings
"""

import pathlib

from fastberry.config import Settings

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]

settings = Settings(base_dir=BASE_DIR)
