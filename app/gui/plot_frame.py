
from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class PlotFrame(Frame):
    """A Frame to hold the matplotlib canvas and a small control panel"""
    def __init__(self, parent):
        super().__init__(parent)
        self.sample = None
        self.plotter = None

        f = Figure(figsize=(5,5), dpi=100)
        self.axes = f.add_subplot(111)
        self.axes.title("RSG")
        self.datacurve = self.axes.plot([],[])[0]
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.show()

        self.control_panel_frame = Frame(self, bd=1)
        self.build()

    def build(self):
        """Build the GUI"""
        self.canvas.get_tk_widget().pack()


    def set_plotter(self, plotter):
        """Change the plot style and controls with a new plotter instance"""
        self.plotter = plotter

    def set_sample(self, sample):
        """Change the sample data"""
        self.sample = sample
