from app.gui.plot.testintervalframe import TestIntervalFrame
from app.project.sample import Sample
from app.util.asc_data import ASCData

from tkinter import *

import sys

from app.util.sample_state import SampleState

assert sys.version_info >= (3, 5)

if __name__ == "__main__":
    root = Tk()
    root.set_state = lambda s: print(s)
    s = Sample()
    s.set_data(ASCData.open("/home/alex/Sample 001 - 66mm - Heat NF 15101937.ASC"))
    f = TestIntervalFrame(root, SampleState(root))
    f.set_sample(s)
    f.pack()
    root.mainloop()