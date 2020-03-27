from tkinter import *


CURR_COLOR = "#00ccc5"
REG_COLOR = "#eff4ff"


def f(x, i):
    return lambda: x.set(i)


class ProgressFrame(Frame):
    """Mimic 'tabs' in a browser window
    control which edit window is showing"""

    def __init__(self, parent, labels, set_frame):
        super().__init__(parent)
        self.set_frame = set_frame
        self.parent = parent
        self.buttons = [
            Button(
                self,
                text=label,
                width=15,
                bg=REG_COLOR,
                activebackground=REG_COLOR,
                command=f(self, i),
            )
            for i, label in enumerate(labels)
        ]
        self.curr = -1
        self.set(0)
        self.build()

    def set(self, i, parent_update=True):
        if self.curr == i:
            return
        update = True
        if parent_update:
            update = self.set_frame(i)
        if update:
            self.buttons[self.curr]["bg"] = REG_COLOR
            self.buttons[i]["bg"] = CURR_COLOR
            self.curr = i

    def build(self):
        for button in self.buttons:
            button.pack(side=LEFT)
