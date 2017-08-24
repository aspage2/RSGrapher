
from tkinter import *


class StateFrame(Frame):
    def __init__(self, parent, dfa):
        super().__init__(parent)
        self.parent = parent
        self.dfa = dfa
        self.sample = None

    def set_sample(self, sample):
        self.sample = sample

    def hide(self):
        pass

    def next(self):
        self.hide()
        self.dfa.next("N")