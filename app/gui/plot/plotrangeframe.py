

from tkinter import *

from app.gui.plot.plot_canvas import PlotCanvas

from matplotlib.figure import Figure

class PlotRangeFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = PlotCanvas(Figure((10,5), dpi=100), self)
        self.sample = None
        self.build()

    def build(self):
        self.canvas.pack()