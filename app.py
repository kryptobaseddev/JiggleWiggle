import os
import sys
from jigglewiggle.gui import JigglerApp
from jigglewiggle.updater import check_for_updates

def resource_path(relative_path):
    """Get the absolute path to a resource, works for development and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load the current version from version.txt
version_file_path = resource_path('version.txt')
try:
    with open(version_file_path, 'r') as f:
        app_version = f.read().strip()
except FileNotFoundError:
    app_version = "1.0.0"  # Default version if version.txt is not found

# Check for updates when the app starts
latest_version = check_for_updates(app_version)

if __name__ == "__main__":
    JigglerApp(app_version, latest_version).run()
