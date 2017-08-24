from tkinter.ttk import Notebook
from tkinter import *

import matplotlib

from app.gui.plot.peakloadframe import PeakLoadFrame
from app.gui.plot.utsframe import UTSFrame
from app.gui.plot.yieldloadframe import YieldLoadFrame
from app.gui.stateframe import StateFrame

matplotlib.use("TkAgg")

GRAPH_DIM = (11, 7)


class FinalPlotFrame(StateFrame):
    def __init__(self, parent, dfa, photodir):
        super().__init__(parent, dfa)
        self.canvasnotebook = Notebook(self)
        self.photodir = photodir
        self.peakloadframe = PeakLoadFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.peakloadframe, text="Peak Load")

        self.utsframe = UTSFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.utsframe, text="Yield Stren/UTS")

        self.yieldloadframe = YieldLoadFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.yieldloadframe, text="Yield Load")

        self.build()

    def set_sample(self, sample):
        super().set_sample(sample)
        self.peakloadframe.set_sample(sample)
        self.utsframe.set_sample(sample)
        self.yieldloadframe.set_sample(sample)

    def ondone(self):
        self.peakloadframe.canvas.figure.savefig("{}S{}_PL.png".format(self.photodir, self.sample.num))
        self.utsframe.canvas.figure.savefig("{}S{}_UTS.png".format(self.photodir, self.sample.num))
        self.yieldloadframe.canvas.figure.savefig("{}S{}_YL.png".format(self.photodir, self.sample.num))

    def build(self):
        self.canvasnotebook.pack()
        Button(self, text="Done", font=("Helvetica", 16), command=self.ondone).pack(side=RIGHT)
