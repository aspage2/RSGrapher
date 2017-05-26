from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import Frame, BOTH, RIGHT, CENTER, Toplevel, Label
from tkinter.ttk import Notebook

from app.datastructure import *

import app.rsgdialog as rsgdialog
import matplotlib
matplotlib.use("TkAgg")

"""
Main Application Window

Subclass of a Tk.Frame to hold the project tools
"""


class ProjectFrame(Frame):
    """The frame holding the project controls, provides handles for modifying project details"""
    GRAPH_SPACE_RATIO = 0.1

    def __init__(self, parent, project_dir=None):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH)

        # Build layout
        self.__child = None
        self.__project = None
        if (project_dir == None):
            self.__build_noproject_layout()
        else:
            self.__trybuildproject(project_dir)

    def __build_project_layout(self):
        """Fill this frame with the controls for this frame's project"""
        self.__child.destroy()
        self.__child = Notebook(self)
        for i in self.__project.samples():
            self.__child.add(SampleFrame(self.__child, i), text=i.name)
        self.__child.pack(fill=BOTH, expand=1)

    def __build_noproject_layout(self):
        """Fill this frame with a 'No Project' indicator"""
        if (self.__child != None):
            self.__child.destroy()
        self.__child = NoProjectFrame(self)

    def noimp(self):
        """Not implemented"""
        print("This function is not implemented.")

    def __open(self):
        """Open a new project"""
        projectdir = rsgdialog.ask_project_dir()
        self.__trybuildproject(projectdir)

    def __close(self):
        if (self.__project != None):
            self.__child.destroy()
            self.__build_noproject_layout()
            self.__project = None

    def __quit(self):
        self.__close()
        self.parent.quit()

    def __trybuildproject(self, project_dir):
        try:
            self.__project = Project(project_dir)
            self.__build_project_layout()
        except:
            rsgdialog.no_file_warning(project_dir)
            self.__build_noproject_layout()

    def __opennewdialog(self, frame):
        self.parent.grab_set()
        newwindow = Toplevel(self.parent)
        frame.setparent(newwindow)

    def __onnewdialogclose(self):
        self.parent.grab_release()


class SampleFrame(Frame):
    """Notebook Frame to show data for a sample for the given project"""

    def __init__(self, parent, sample):
        super().__init__(parent)
        self.__sample = sample
        self.pack(fill=BOTH)
        self.__build()

    def __build(self):
        f = Figure(figsize=(5, 5), dpi=100)
        p = f.add_subplot(111)
        self.__stresscurve, = p.plot(self.__sample.get_disp_data(), self.__sample.get_load_data())

        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)


class NoProjectFrame(Frame):
    """Simple frame used when a project is not open"""
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH)
        Label(self, text="No Projects are Open").pack(anchor=CENTER)
