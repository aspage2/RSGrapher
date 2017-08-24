from app.gui.plot.elasticintervalframe import ElasticIntervalFrame
from app.gui.plot.finalplotframe import FinalPlotFrame
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
    s.set_data(ASCData.open("D:\\samples\\RSG Sample Projects\\RSG 0283 - DSI - 66 mm Threadbar (Heat NF15101937) RTT\\Raw Data\\Sample 002 - 66mm - Heat NF 15101937.ASC"))
    s.zero = 0.1
    s.length = 45.0
    s.area = 5.0
    s.set_elastic_zone(200000.0, 400000.0)
    s.plotrange[:] = (5.0, 1000000)
    f = FinalPlotFrame(root, SampleState(None))
    f.pack()
    f.set_sample(s)
    root.mainloop()