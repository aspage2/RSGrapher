from tkinter import *


class PlotRangeInputGroup(Frame):
    """Specify the MAX value (load/displacement) to show on the final plot"""

    def __init__(self, parent, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.loadmax = Entry(self, width=8, font=font)
        self.dispmax = Entry(self, width=8, font=font)
        Label(self, text="Disp (in.):", font=font).pack(side=LEFT, padx=10)
        self.dispmax.pack(side=LEFT)
        Label(self, text="Load (lbs.):", font=font).pack(side=LEFT, padx=10)
        self.loadmax.pack(side=LEFT)

    @property
    def plotrange(self):
        if not self.entries_valid():
            raise ValueError("Attempt to get invalid plotting range")
        return float(self.dispmax.get()), float(self.loadmax.get())

    def set_plotrange(self, dm, lm):
        self.loadmax.delete(0, END)
        if lm is not None:
            self.loadmax.insert(0, str(lm))
        self.dispmax.delete(0, END)
        if dm is not None:
            self.dispmax.insert(0, str(dm))

    def entries_valid(self):
        try:
            # Fails on empty strings as well
            float(self.loadmax.get())
            float(self.dispmax.get())
        except:
            return False
        return True
