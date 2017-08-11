
from tkinter import *

from app.gui import PANEL_BG

ENTRY_WIDTH = 40

class TitleInputGroup(Frame):
    def __init__(self, parent, bg=PANEL_BG, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.titles = []
        for i in range(1, 4):
            self.titles.append(Entry(self, width=ENTRY_WIDTH))
            Label(self, text="Title {}".format(i), bg=bg).pack()
            self.titles[i-1].pack()

    def get_titles(self):
        return (t.get() for t in self.titles)

    def entries_valid(self):
        if self.titles[0].get() == "":
            return False
        return True