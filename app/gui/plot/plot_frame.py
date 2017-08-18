from tkinter import *

import matplotlib

from app.gui.plot.elasticintervaltool import ElasticIntervalTool
from app.gui.plot.plot_tool import Focus
from app.gui.plot.testintervaltool import TestIntervalTool

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
        self.nav = NavigationToolbar2TkAgg(self.canvas, self)
        self.controlframe = Frame(self, relief=SUNKEN, border=2, bg=PANEL_BG)
        self.controllabel = Label(self.controlframe, font=("Helvetica", 10), bg=PANEL_BG)
        self.testinterval = TestIntervalTool(self.canvas, self.nav, self.controllabel)
        self.elasticinterval = ElasticIntervalTool(self.canvas, self.nav, self.controllabel)
        self.currtool = self.testinterval
        self.sample = None
        self.build()

    def set_sample(self, sample):
        self.sample = sample
        self.canvas.set_data(sample.data.disp, sample.data.load)
        self.canvas.set_labels("Load vs Displacement", "Displacement (in.)", "Load (lbs.)")
        self.canvas.figure.tight_layout()
        self.canvas.show()
        self.testinterval.set_sample(sample)
        self.elasticinterval.set_sample(sample)

    def set_test_interval(self):
        self.currtool.hide()
        self.currtool = self.testinterval
        self.currtool.show()

    def set_elastic_interval(self):
        self.currtool.hide()
        self.currtool = self.elasticinterval
        self.currtool.show()

    def build(self):
        """Build the UI"""
        bframe = Frame(self.controlframe, bg=PANEL_BG)
        bframe.f1 = Frame(bframe, bg=PANEL_BG)
        bframe.f2 = Frame(bframe, bg=PANEL_BG)
        Button(bframe.f1, text="Test Interval", command=self.set_test_interval).pack(side=LEFT)
        Button(bframe.f1, text="Elastic Interval", command=self.set_elastic_interval).pack(side=LEFT)
        Button(bframe.f2, text="Set Lower Bound", command=lambda: self.currtool.set_focus(Focus.Lo)).pack(side=LEFT)
        Button(bframe.f2, text="Set Upper Bound", command=lambda: self.currtool.set_focus(Focus.Hi)).pack(side=LEFT)
        Button(bframe.f2, text="Set Neither", command=lambda: self.currtool.set_focus(Focus.Neither)).pack(side=LEFT)
        bframe.f1.pack()
        bframe.f2.pack()
        bframe.pack(side=LEFT, padx=10)
        self.controllabel.pack(side=LEFT, padx=10)
        self.canvas.pack()
        self.nav.pack()
        self.controlframe.pack(fill=X,ipady=10)
