from tkinter.ttk import Notebook
from tkinter import *

import matplotlib

from app.gui.plotting.peakloadframe import PeakLoadFrame
from app.gui.plotting.utsframe import UTSFrame
from app.gui.plotting.yieldloadframe import YieldLoadFrame
from app.gui.abstract_tab_frame import AbstractTabFrame

matplotlib.use("TkAgg")

class FinalPlotFrame(AbstractTabFrame):
    def __init__(self, parent, photodir):
        super().__init__(parent, "Final Plots")
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
        self.next()

    def build(self):
        self.canvasnotebook.pack()
        Button(self, text="Generate PNGs", font=("Helvetica", 16), command=self.ondone).pack(side=RIGHT)
