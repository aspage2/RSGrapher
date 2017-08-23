
from tkinter import *

from app.gui.stateframe import StateFrame


class InfoFrame(StateFrame):
    def __init__(self, parent, dfa):
        super().__init__(parent, dfa)

    def set_sample(self, sample):
        super().set_sample(sample)