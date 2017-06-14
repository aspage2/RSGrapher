from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import Frame, BOTH, RIGHT, CENTER, Label

import matplotlib
matplotlib.use("TkAgg")

"""
Main Application Window

Subclass of a Tk.Frame to hold the project tools
"""


class ProjectFrame(Frame):
    """The frame holding the project controls, provides handles for modifying project details"""
    GRAPH_SPACE_RATIO = 0.1

    def __init__(self, parent, project=None):
        super().__init__(parent)
        self.project = project
        self.parent = parent
        self.build()
        self.refresh()
        self.pack(fill=BOTH)

    def build(self):
        pass
    def refresh(self):
        pass


class SampleFrame(Frame):
    """Notebook Frame to show data for a sample for the given project"""

    def __init__(self, parent, sample):
        super().__init__(parent)
        self.sample = sample
        self.pack(fill=BOTH)
        self.build()

    def build(self):
        f = Figure(figsize=(5, 5), dpi=100)
        p = f.add_subplot(111)
        p.set_xlabel("Time (s)")
        p.set_ylabel("Displacement (in)")
        p.set_title("Raw Data")
        self.stresscurve, = p.plot(self.sample.get_disp_data(), self.sample.get_load_data())

        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=True)


class NoProjectFrame(Frame):
    """Simple frame used when a project is not open"""
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH)
        Label(self, text="No Projects are Open").pack(anchor=CENTER)
