import sys
import argparse

from app.main import application_debug, application_start

assert sys.version_info >= (3, 5)

if __name__ == "__main__":
    application_start()
