
from tkinter import *


class SampleDimensionInputGroup(Frame):
    """Input sample dimensions (area, length)"""
    def __init__(self, parent, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.len_entry = Entry(self, width=6, font=font)
        self.area_entry = Entry(self, width=6, font=font)

        Label(self, text="Len (in.):", font=font).pack(side=LEFT)
        self.len_entry.pack(side=LEFT)
        Label(self, text="Area (sq. in.)", font=font).pack(side=LEFT)
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

    def set_area(self, area):
        self.area_entry.delete(0, END)
        if area is not None:
            self.area_entry.insert(0, str(area))

    def set_length(self, length):
        self.len_entry.delete(0, END)
        if length is not None:
            self.len_entry.insert(0, str(length))

    def get_area(self):
        return float(self.area_entry.get())
    def get_length(self):
        return float(self.len_entry.get())

