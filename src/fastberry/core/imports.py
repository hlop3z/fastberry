import os
import sys
from pathlib import Path

try:
    # Get "main.py" <FILE>
    MAIN = sys.modules.get("main")
    if MAIN:
        BASE_DIR = Path(MAIN.__file__).resolve().parent
    else:
        BASE_DIR = Path(sys.argv[0]).resolve().parent

    print(BASE_DIR)
    # Append "PROJECT" <Folder>
    sys.path.insert(0, os.path.join(BASE_DIR, "project"))

    # Import settings.py <FILE>
    from project import settings

    # Get "INSTALLED-APPS"
    if hasattr(settings, "INSTALLED_APPS"):
        INSTALLED_APPS = settings.INSTALLED_APPS
    else:
        INSTALLED_APPS = []

    # Include apps/
    sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
except:
    raise Exception("Please create the <folder> ./project and the settings.py <file>.")
