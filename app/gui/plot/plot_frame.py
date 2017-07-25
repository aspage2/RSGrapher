from tkinter import *

import matplotlib
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
        self.nav = NavigationToolbar2TkAgg(self.canvas,self)

        self.descrip = Label(self,text="<NO SAMPLE DATA>",font=("Helvetica",16))
        self.build()

    def set_sample(self, sample):
        """Set the sample of this frame to the argument. """
        if sample is None:
            self.descrip.config(text="<NO SAMPLE DATA>")
        else:
            self.descrip.config(text="Name: {0}  Area: {1} sq.in.  Length: {2} in.".format(sample.name, sample.area, sample.length))

    def build(self):
        """Build the UI"""
        self.descrip.pack()
        self.canvas.pack()
        self.nav.pack()
        self.controlframe.pack(fill=X)
