from tkinter import *

import matplotlib

from app.gui.input_group.sample_dir_input import SampleDirectoryInputGroup

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from app.gui import PANEL_BG
from app.gui.plot.plot_canvas import PlotCanvas


class PlotFrame(Frame):
    """Base class for a frame containing plot functions."""

    def __init__(self, parent, title="RSG", xlabel="", ylabel=""):
        super().__init__(parent, padx=10)
        self.canvas = PlotCanvas(Figure(figsize=(8, 5), dpi=100), self)
        self.canvas.set_labels(title, xlabel, ylabel)
        self.canvas.figure.tight_layout()
        self.canvas.show()
        self.controlframe = Frame(self, relief=SUNKEN, border=2, bg=PANEL_BG)
        self.dir_input = SampleDirectoryInputGroup(self.controlframe)
        self.nav = NavigationToolbar2TkAgg(self.canvas,self)

        self.build()

    def build(self):
        """Build the UI"""
        self.dir_input.pack(side=LEFT)
        self.canvas.pack()
        self.nav.pack()
        self.controlframe.pack(fill=X, ipadx=10, ipady=10)
