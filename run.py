import sys

assert sys.version_info >= (3, 5)

from app.root import ApplicationInstance

if __name__ == "__main__":
    ApplicationInstance.start()
