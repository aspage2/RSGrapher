from tkinter import *


class SampleNumberInputGroup(Frame):
    """Input sample number, which MUST be a positive whole number"""

    def __init__(self, parent, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.sample_num = Entry(self, width=3, font=font)
        Label(self, text="Sample # ", font=font).pack(side=LEFT)
        self.sample_num.pack(side=LEFT)
        self.re = re.compile("^\d+$")

    def set(self, i):
        self.sample_num.delete(0, END)
        self.sample_num.insert(0, str(i))

    def get_num(self):
        return int(self.sample_num.get())

    def entries_valid(self):
        if self.sample_num.get() == "":
            return False
        return re.match("^\d+$", self.sample_num.get()) is not None
