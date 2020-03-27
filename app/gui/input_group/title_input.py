from tkinter import *


ENTRY_WIDTH = 40


class TitleInputGroup(Frame):
    """Enter 3 plot titles, with the first being mandatory"""

    def __init__(self, parent, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.titles = []
        for i in range(1, 4):
            self.titles.append(Entry(self, width=ENTRY_WIDTH, font=font))
            Label(self, text="Title {}".format(i), font=font).pack()
            self.titles[i - 1].pack()

    def set_titles(self, *t):
        for i, title in enumerate(t):
            self.titles[i].delete(0, END)
            if title is not None:
                self.titles[i].insert(0, title)

    def get_titles(self):
        return (t.get() for t in self.titles)

    def entries_valid(self):
        if self.titles[0].get() == "":
            return False
        return True
