from tkinter import *

from app.gui import PANEL_BG
from app.gui.input_group.sample_dim_input import SampleDimensionInputGroup
from app.gui.input_group.sample_dir_input import SampleDirectoryInputGroup
from app.gui.input_group.sample_num_input import SampleNumberInputGroup
from app.gui.input_group.title_input import TitleInputGroup
from app.gui.plot.finalgraphviewer import FinalPlotWindow
from app.gui.plot.plot_frame import PlotFrame


class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent, project=None):
        super().__init__(parent, padx=10, pady=10)
        self.project = project
        self.parent = parent

        pad = {"padx":10, "pady":10}

        self.plot_panel = PlotFrame(self)

        self.input_panel = Frame(self, bg=PANEL_BG, borderwidth=2, relief=SUNKEN)
        self.title_input = TitleInputGroup(self.input_panel, bg=PANEL_BG,**pad)
        self.dim_input = SampleDimensionInputGroup(self.input_panel, bg=PANEL_BG,**pad)
        self.num_input = SampleNumberInputGroup(self.input_panel, bg=PANEL_BG,**pad)
        self.dir_input = SampleDirectoryInputGroup(self.input_panel, self.plot_panel, bg=PANEL_BG, **pad)

        self.build()

    def open_graph_window(self):
        if self.dim_input.entries_valid():
            self.plot_panel.sample.length = self.dim_input.get_length()
            self.plot_panel.sample.area = self.dim_input.get_area()
        # else:
        #     messagebox.showwarning(title="Show Graphs", message="User must input title, sample number and dimensions")
        #     return
        w = FinalPlotWindow(self, self.plot_panel.sample)
        w.grab_set()
        self.wait_window(w)

    def build(self):
        self.title_input.pack()
        self.dim_input.pack()
        self.num_input.pack()
        self.dir_input.pack()
        Button(self.input_panel, font=("Helvetica", 16), text="Graphs", command=self.open_graph_window).pack(anchor=N)
        self.input_panel.pack(side=LEFT,fill=Y)
        self.plot_panel.pack(side=LEFT)
