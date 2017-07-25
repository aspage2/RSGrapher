from app.gui import PANEL_BG
from app.gui.plot.plot_frame import PlotFrame

from tkinter import Label


class EmptyPlotFrame(PlotFrame):
    """No functionality; a placeholder for when a project has no samples yet or if a project isn't open"""

    def __init__(self, parent):
        super().__init__(parent, None)
        Label(self.controlframe, text=" ", bg=PANEL_BG).pack()
