from tkinter.ttk import Notebook

import matplotlib

from app.gui.dialog import BaseDialogWindow
from app.gui.plot.peakloadframe import PeakLoadFrame
from app.gui.plot.utsframe import UTSFrame
from app.gui.plot.yieldloadframe import YieldLoadFrame


matplotlib.use("TkAgg")

GRAPH_DIM = (11, 7)

class FinalPlotWindow(BaseDialogWindow):
    def __init__(self, parent, sample):
        super().__init__(parent)
        self.sample = sample
        self.canvasnotebook = Notebook(self)

        self.peakloadframe = PeakLoadFrame(self.canvasnotebook, self.sample)
        self.canvasnotebook.add(self.peakloadframe, text="Peak Load")

        self.utsframe = UTSFrame(self.canvasnotebook, sample)
        self.canvasnotebook.add(self.utsframe, text="Yield Stren/UTS")

        self.yieldloadcanvas = YieldLoadFrame(self.canvasnotebook, sample)
        self.canvasnotebook.add(self.yieldloadcanvas, text="Yield Load")

        self.build()

    def build(self):
        self.canvasnotebook.pack()
