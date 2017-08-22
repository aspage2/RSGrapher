
from tkinter import *


class ChangeableFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.modified = True

    def set_modified(self, val):
        self.modified = val

    def is_modified(self):
        return self.modified