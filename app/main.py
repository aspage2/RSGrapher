
from app.gui.root import ApplicationWindow

application_running = False

DEFAULT_GEOMETRY="1080x720+300+300"


def application_start():
    tk = ApplicationWindow(DEFAULT_GEOMETRY)
    tk.run()

def application_debug():
    tk = ApplicationWindow(DEFAULT_GEOMETRY)
    tk.run()