
from tkinter import *

from app.gui.input_group.title_input import TitleInputGroup
from app.gui.input_group.sample_dim_input import SampleDimensionInputGroup
from app.gui.input_group.plot_range_input import PlotRangeInputGroup
from app.gui.stateframe import StateFrame

FONT = ("Helvetica", 16)

class InfoFrame(StateFrame):
    def __init__(self, parent, dfa):
        super().__init__(parent, dfa)
        self.titleinput = TitleInputGroup(self, font=FONT)
        self.diminput = SampleDimensionInputGroup(self, font=FONT)
        self.plotrange = PlotRangeInputGroup(self, font=FONT)
        self.build()

    def ondone(self):
        if not self.titleinput.entries_valid():
            print("INVALID ENTRIES")
            return
        elif not self.diminput.entries_valid():
            print("INVALID DIM")
            return
        elif not self.plotrange.entries_valid():
            print("INVALID PLOTRANGE")
            return

        self.next()

    def hide(self):
        self.sample.titles[:] = self.titleinput.get_titles()
        self.sample.area = self.diminput.get_area()
        self.sample.length = self.diminput.get_length()
        self.sample.plotrange[:] = self.plotrange.plotrange

    def build(self):
        self.titleinput.pack(pady=10)
        Label(self, text="Sample Dimensions", font=FONT).pack(pady=10)
        self.diminput.pack(pady=10)
        Label(self, text="Plot Maxima", font=FONT).pack(pady=10)
        self.plotrange.pack(pady=10)
        Button(self, text="Done", font=FONT, command=self.ondone).pack()