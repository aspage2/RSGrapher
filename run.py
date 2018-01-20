
from app.gui.app_window import AppWindow

import sys

from app.project.project_dir import ProjectDirectory

assert sys.version_info >= (3, 5)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = ProjectDirectory.open_project(sys.argv[1])
    else:
        p = None
    root = AppWindow(p)
    root.run()