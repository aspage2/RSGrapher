import sys
import argparse

from app.gui.root import ApplicationWindow

assert sys.version_info >= (3, 5)

if __name__ == "__main__":
    tk = ApplicationWindow("1080x720")
    tk.run()
