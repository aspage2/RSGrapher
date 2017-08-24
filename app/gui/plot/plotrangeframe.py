from tkinter import *

from app.gui.plot.plot_canvas import PlotCanvas

from matplotlib.figure import Figure


class PlotRangeFrame(Frame):
    def __init__(self, parent, title="RSG"):
        super().__init__(parent)
        self.canvas = PlotCanvas(Figure((10, 6), dpi=100), self)
        self.title = title
        self.sample = None
        self.build()

    def set_sample(self, sample):
        self.sample = sample
        title = sample.titles[0]
        t = 1
        while t != 3 and sample.titles[t] is not None and sample.titles[t] != "":
            title += "\n" + sample.titles[t]
            t += 1
        if title is None:
            title = ""
        title += "\n"+self.title+" (Sample {})".format(sample.num)
        self.canvas.set_labels(title=title)
        self.canvas.show()

    def build(self):
        self.canvas.pack()
