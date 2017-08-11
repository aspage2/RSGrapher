
from app.gui.input_group.title_input import TitleInputGroup
from tkinter import *
from tkinter import messagebox
import logging

from app.gui import PANEL_BG
from app.gui.input_group.sample_dim_input import SampleDimensionInputGroup
from app.gui.input_group.sample_num_input import SampleNumberInputGroup
from app.gui.plot.plot_frame import PlotFrame

RADIO_BUTTON_STUFF = (("Test Interval", 1, lambda m: lambda: m.set_plot_frame(1)),
                      ("Elastic Interval", 2, lambda m: lambda: m.set_plot_frame(2)),
                      ("Load vs. Displacement", 3, lambda m: lambda: m.set_plot_frame(3)),
                      ("Stress vs. Strain (UTS)", 4, lambda m: lambda: m.set_plot_frame(4)),
                      ("Stress vs. Strain (Yield)", 5, lambda m: lambda: m.set_plot_frame(5)),
                      ("Load vs. Strain", 6, lambda m: lambda: m.set_plot_frame(6)))


class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent, project=None):
        super().__init__(parent, padx=10, pady=10)
        self.project = project
        self.parent = parent

        pad = {"padx":10, "pady":10}

        self.input_panel = Frame(self, bg=PANEL_BG, borderwidth=2, relief=SUNKEN)
        self.title_input = TitleInputGroup(self.input_panel, bg=PANEL_BG,**pad)
        self.dim_input = SampleDimensionInputGroup(self.input_panel, bg=PANEL_BG,**pad)
        self.num_input = SampleNumberInputGroup(self.input_panel, bg=PANEL_BG,**pad)

        self.plot_panel = PlotFrame(self)
        self.build()

    def build(self):
        self.title_input.pack()
        self.dim_input.pack()
        self.num_input.pack()
        self.input_panel.pack(side=LEFT,fill=Y)
        self.plot_panel.pack(side=LEFT)
