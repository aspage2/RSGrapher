
from tkinter import *

from app.gui import GUI_FONT
from app.gui.frame.abstract_tab_frame import AbstractTabFrame
from app.gui.input_group.plot_range_input import PlotRangeInputGroup
from app.gui.input_group.precision_input import PrecisionInputGroup
from app.gui.input_group.sample_dim_input import SampleDimensionInputGroup
from app.gui.input_group.title_input import TitleInputGroup


class BasicInfoFrame(AbstractTabFrame):
    """Sample information: plotting titles, sample dimensions, plotting range"""
    def __init__(self, parent, handler, next_frame):
        super().__init__(parent, "Info", handler, next_frame)
        self.title_input = TitleInputGroup(self, font=GUI_FONT)
        self.dim_input = SampleDimensionInputGroup(self, font=GUI_FONT)
        self.plot_range_input = PlotRangeInputGroup(self, font=GUI_FONT)
        self.precision_input = PrecisionInputGroup(self, font=GUI_FONT)
        self.build()

    def content_update(self):
        s = self._proj_handle.curr_sample
        if s is None:
            return
        if None not in s.titles:
            self.title_input.set_titles(*s.titles)
        if s.area is not None:
            self.dim_input.set_area(s.area)
        if s.length is not None:
            self.dim_input.set_length(s.length)

        self.precision_input.set(s.precision)
        if None not in s.plotrange:
            self.plot_range_input.set_plotrange(*s.plotrange)

    def is_done(self):
        """"""
        return self.title_input.entries_valid() and self.dim_input.entries_valid() and self.plot_range_input.entries_valid()

    def unload(self):
        """Called by AbstractTabFrame.on_next
        is_done is true if unload is called."""
        s = self._proj_handle.curr_sample
        if s is None:
            return
        s.titles[:] = self.title_input.get_titles()
        s.area = self.dim_input.get_area()
        s.length = self.dim_input.get_length()
        s.plotrange[:] = self.plot_range_input.plotrange
        s.precision = self.precision_input.precision

    def build(self):
        self.title_input.pack(pady=10)
        Label(self, text="Sample Dimensions", font=GUI_FONT).pack(pady=10)
        self.dim_input.pack(pady=10)
        Label(self, text="Plot Maxima", font=GUI_FONT).pack(pady=10)
        self.plot_range_input.pack(pady=10)
        self.precision_input.pack(pady=10)
        Button(self, text="Done", font=GUI_FONT, command=self.on_next).pack()