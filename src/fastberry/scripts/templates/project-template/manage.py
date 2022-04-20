#!/usr/bin/env python
"""
Project Manager
"""

import pathlib

from fastberry import Fastberry

BASE_DIR = pathlib.Path(__file__).resolve().parents[0]

manager = Fastberry(base_dir=BASE_DIR, is_cli=True)

if __name__ == "__main__":
    manager.cli()
