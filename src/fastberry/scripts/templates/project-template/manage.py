#!/usr/bin/env python
"""
Project Manager
"""

import pathlib

from fastberry.config import Settings

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = pathlib.Path(__file__).resolve().parents[0]

# Import API-Settings
settings = Settings(base_dir=BASE_DIR, is_cli=True)

if __name__ == "__main__":
    settings.cli()
