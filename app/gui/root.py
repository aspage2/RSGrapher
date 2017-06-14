from tkinter import Tk, Frame, Menu, BOTH

from app.gui.project_frame import ProjectFrame
from app.project.helper import Helper
from app.project.datastructure import Project


class ApplicationWindow(Tk):
    """A running instance of the RSGrapher application. Only one instance may be run at a time"""

    def __init__(self, geometry):
        super().__init__()
        self.title("RSGrapher")
        self.geometry(geometry)
        self.iconbitmap("res/window_icon.ico")
        p = Project()
        self.helper = Helper(p, ProjectFrame(self, p))
        self.bind_menu_actions()

    def __del__(self):
        ApplicationWindow.running = False

    def bind_menu_actions(self):
        """Create menu bar"""
        menubar = Menu(self)
        self.config(menu=menubar)

        # File menu
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="New", command=self.helper.new)
        filemenu.add_command(label="Open Project", command=self.helper.open)
        filemenu.add_separator()
        filemenu.add_command(label="Export Graphs", command=self.helper.export)
        filemenu.add_separator()
        filemenu.add_command(label="Close Project", command=self.helper.close)
        filemenu.add_command(label="Quit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Project Menu
        projectmenu = Menu(menubar, tearoff=False)
        projectmenu.add_command(label='Add Sample', command=self.helper.add_sample)
        projectmenu.add_command(label='Add Photo to Sample', command=self.helper.noimp)
        menubar.add_cascade(label="Project", menu=projectmenu)

    def exit(self):
        self.destroy()

    def run(self):
        """Run this application"""
        self.mainloop()
