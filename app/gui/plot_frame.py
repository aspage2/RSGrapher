from tkinter import *

from app.gui import PANEL_BG
from app.gui.plot_canvas import PlotCanvas

from matplotlib.figure import Figure

from app.util.plotter import EmptyPlotter


class PlotFrame(Frame):
    """A frame to house the plot and plot controllers"""

    def __init__(self, parent):
        super().__init__(parent, padx=10)
        self.canvas = PlotCanvas(Figure(figsize=(5, 5), dpi=100), self)
        self.controlframe = Frame(self, relief=SUNKEN, border=2, bg=PANEL_BG)
        self.plotter = None
        self.set_plotter(None)
        self.build()

    def build(self):
        self.canvas.pack()
        self.controlframe.pack(fill=X)

    def set_plotter(self, plotter):
        if self.plotter is not None:
            self.plotter.cleanup()
        if plotter is None:
            self.plotter = EmptyPlotter(self)
        else:
            self.plotter = plotter
        self.plotter.run()
