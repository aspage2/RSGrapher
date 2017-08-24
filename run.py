from app.gui.plot.elasticintervalframe import ElasticIntervalFrame
from app.gui.plot.finalplotframe import FinalPlotFrame
from app.gui.plot.testintervalframe import TestIntervalFrame
from app.gui.root import ApplicationWindow
from app.project.sample import Sample
from app.util.asc_data import ASCData

from tkinter import *

import sys

from app.util.sample_state import SampleState

assert sys.version_info >= (3, 5)

if __name__ == "__main__":
    root = ApplicationWindow()
    root.run()