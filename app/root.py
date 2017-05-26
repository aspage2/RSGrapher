from tkinter import Tk, Frame, Menu, BOTH

from app.project import ProjectFrame


class ApplicationInstance(Tk):
    """A running instance of the RSGrapher application. Only one instance may be run at a time"""

    running = False

    @staticmethod
    def start(geometry="500x500+300+300", projectdir=None):
        """Run an application instance without debug logging."""
        app = ApplicationInstance(geometry, projectdir)
        app.run()

    @staticmethod
    def debug(geometry="500x500+300+300", projectdir=None):
        """Run an application instance with debug logging enabled."""
        app = ApplicationInstance(geometry, projectdir, debug=True)

    def __init__(self, geometry, projectdir=None, debug=False):
        assert not ApplicationInstance.running
        super().__init__()
        ApplicationInstance.running = True
        self.title("RSGrapher")
        self.geometry(geometry)
        self.root = MenuFrame(self)
        self.project = ProjectFrame(self.root, projectdir)
        self.root.bind_menu_actions(self.project)

    def __del__(self):
        ApplicationInstance.running = False

    def run(self):
        """Run this application"""
        self.mainloop()


class MenuFrame(Frame):
    """The root frame in the application window."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH)

    def bind_menu_actions(self, frame):
        """Create menu bar"""
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        # File menu
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="New", command=frame.noimp)
        filemenu.add_command(label="Open Project", command=frame.noimp)
        filemenu.add_command(label="Save", command=frame.noimp)
        filemenu.add_separator()
        filemenu.add_command(label="Export Graphs")
        filemenu.add_separator()
        filemenu.add_command(label="Close Project")
        filemenu.add_command(label="Quit")
        menubar.add_cascade(label="File", menu=filemenu)

        # Project Menu
        projectmenu = Menu(menubar, tearoff=False)
        projectmenu.add_command(label='Add Sample', command=frame.noimp)
        menubar.add_cascade(label="Project", menu=projectmenu)