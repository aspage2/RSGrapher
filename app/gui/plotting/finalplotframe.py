from tkinter.ttk import Notebook
from tkinter import *

import matplotlib

from app.gui.plotting.peakloadframe import PeakLoadFrame
from app.gui.plotting.utsframe import UTSFrame
from app.gui.plotting.yieldloadframe import YieldLoadFrame
from app.gui.abstract_tab_frame import AbstractTabFrame

matplotlib.use("TkAgg")


class FinalPlotFrame(AbstractTabFrame):
    def __init__(self, parent, photo_dir, handler, next_frame):
        super().__init__(parent, "Final Plots", handler, next_frame)
        self.canvasnotebook = Notebook(self)
        self.photodir = photo_dir
        self.peakloadframe = PeakLoadFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.peakloadframe, text="Peak Load")

        self.utsframe = UTSFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.utsframe, text="Yield Stren/UTS")

        self.yieldloadframe = YieldLoadFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.yieldloadframe, text="Yield Load")

        self.build()

    def content_update(self):
        s = self._proj_handle.curr_sample
        self.peakloadframe.set_sample(s)
        self.utsframe.set_sample(s)
        self.yieldloadframe.set_sample(s)

    def unload(self):
        s = self._proj_handle.curr_sample
        self.peakloadframe.canvas.figure.savefig("{}S{}_PL.pdf".format(self.photodir, s.num))
        self.utsframe.canvas.figure.savefig("{}S{}_UTS.pdf".format(self.photodir, s.num))
        self.yieldloadframe.canvas.figure.savefig("{}S{}_YL.pdf".format(self.photodir, s.num))


    def build(self):
        self.canvasnotebook.pack()
        Button(self, text="Generate PNGs", font=("Helvetica", 16), command=self.on_next).pack(side=RIGHT)
