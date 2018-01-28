from tkinter import *


CURR_COLOR = "#00ccc5"
REG_COLOR = "#eff4ff"


def f(x, i):
    return lambda: x.set(i)

class ProgressFrame(Frame):
    def __init__(self, parent, labels):
        super().__init__(parent)
        self.parent = parent
        self.buttons = [Button(self, text=label, width=15, bg=REG_COLOR, activebackground=REG_COLOR,
                   command=f(self, i)) for i, label in enumerate(labels)]
        self.curr = -1
        self.set(0)
        self.build()

    def set(self, i, parent_update=True):
        if self.curr == i:
            return
        self.buttons[self.curr]['bg'] = REG_COLOR
        self.buttons[i]['bg'] = CURR_COLOR
        self.curr = i
        if parent_update:
            self.parent.set_frame(i)

    def build(self):
        for button in self.buttons:
            button.pack(side=LEFT)
