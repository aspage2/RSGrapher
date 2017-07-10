
from tkinter import *

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""
    def __init__(self, parent):
        super().__init__(parent)
        self.project = None
        self.build()

    def build(self):
        """Build the user interface"""
        pass

    def refresh_project_info(self):
        """Update the GUI to reflect changes in
           project information (extraneous info)"""
        pass

    def set_sample(self):
        """Set the """