
from tkinter import *

from app.gui import PANEL_BG


class SampleNumberInputGroup(Frame):
    def __init__(self, parent, bg=PANEL_BG, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.sample_num = Entry(self, width=3)
        Label(self, text="Sample # ", bg=bg).pack(side=LEFT)
        self.sample_num.pack(side=LEFT)
        self.re = re.compile("^\d$")

    def get_num(self):
        return int(self.sample_num.get())

    def entries_valid(self):
        if self.sample_num.get() == "":
            return False
        return re.match("^\d+$", self.sample_num.get()) is not None