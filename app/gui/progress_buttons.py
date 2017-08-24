from tkinter import *

from app.util.progress_enum import Prog

CURR_COLOR = "#00ccc5"
REG_COLOR = "#eff4ff"


class ProgressFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        labels = ["Info", "Test Data", "Trim Data", "Elastic Zone", "Graphs"]
        self.buttons = [Button(self, text=labels[i], width=15, bg=REG_COLOR, activebackground=REG_COLOR) for i in
                        range(5)]
        self.curr = 0
        self.set(Prog.INFO)
        self.build()

    def set(self, val):
        if val is None:
            return
        i = val.value
        self.buttons[self.curr]['bg'] = REG_COLOR
        self.buttons[i]['bg'] = CURR_COLOR
        self.curr = i

    def build(self):
        for button in self.buttons:
            button.pack(side=LEFT)
