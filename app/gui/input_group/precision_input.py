
from tkinter import *


class PrecisionInputGroup(Frame):
    def __init__(self, parent, font):
        super().__init__(parent)
        self._var = IntVar(0)
        self._buttons = []
        f = Frame(self)
        for i in range(3):
            r = Radiobutton(f, variable=self._var, val=i, text="{}".format(10 ** i),font=font)
            self._buttons.append(r)
            r.pack(side=LEFT)
        Label(self, text="Precision (lbs.)",font=font).pack()
        f.pack()

    def set(self, precision):
        if precision is not None:
            self._var.set(precision)

    @property
    def precision(self):
        return self._var.get()
