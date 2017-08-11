
from tkinter import *

from app.gui import PANEL_BG


class SampleDimensionInputGroup(Frame):
    def __init__(self, parent, bg=PANEL_BG, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.len_entry = Entry(self, width=6)
        self.area_entry = Entry(self, width=6)

        Label(self, text="Len (in.):", bg=bg).pack(side=LEFT)
        self.len_entry.pack(side=LEFT)
        Label(self, text="Area (sq. in.)", bg=bg).pack(side=LEFT)
        self.area_entry.pack(side=LEFT)

    def entries_valid(self):
        if self.len_entry.get() == "" or self.area_entry.get() == "":
            return False
        try:
            float(self.len_entry.get())
            float(self.area_entry.get())
        except:
            return False
        return True

    def get_area(self):
        return float(self.area_entry.get())
    def get_length(self):
        return float(self.len_entry.get())

