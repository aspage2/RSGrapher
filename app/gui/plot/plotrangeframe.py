

from tkinter import *

from app.gui.plot.plot_canvas import PlotCanvas

from matplotlib.figure import Figure

class PlotRangeFrame(Frame):
    def __init__(self, parent, sample):
        super().__init__(parent)
        self.canvas = PlotCanvas(Figure((11,7), dpi=100), self)
        self.sample = sample
        self.f = Frame(self)
        self.xrange = Entry(self.f, width=15, font=("Helvetica",16))
        self.xrange.bind("<Return>", lambda e: self.canvas.set_xrange(0, float(self.xrange.get())))
        self.yrange = Entry(self.f, width=15, font=("Helvetica",16))
        self.yrange.bind("<Return>", lambda e: self.canvas.set_yrange(0, float(self.yrange.get())))

        self.init()
        self.build()

    def get_range(self):
        return float(self.xrange.get()), float(self.yrange.get())

    def init(self):
        raise NotImplementedError()

    def build(self):
        self.canvas.pack()
        Label(self.f, text="X: ").pack(side=LEFT)
        self.xrange.pack(side=LEFT)
        Label(self.f, text="Y: ").pack(side=LEFT)
        self.yrange.pack(side=LEFT)
        self.f.pack(pady=10)