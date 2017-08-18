
from tkinter import *

from app.gui.plot.finalgraphviewer import FinalPlotWindow
from app.project.sample import Sample
from app.util.asc_data import ASCData
from app.util.auto_elastic import suggested_elastic_zone

if __name__ == "__main__":
    root= Tk()
    s = Sample(ASCData.open("D:\\samples\\RSG Sample Projects\\RSG 0283 - DSI - 66 mm Threadbar (Heat NF15101937) RTT\\Raw Data\\Sample 002 - 66mm - Heat NF 15101937.ASC"))
    s.length = 43.75
    s.area = 5.16
    s.set_elastic_interval(*suggested_elastic_zone(*s.elastic_interval_data()[1:]))
    f = FinalPlotWindow(root, s)
    root.mainloop()