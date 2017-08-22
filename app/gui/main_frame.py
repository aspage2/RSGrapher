from tkinter import *

from app.gui.progress_buttons import ProgressFrame
from app.util.sample_state import SampleState
from app.util.progress_enum import Prog

class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent, project):
        super().__init__(parent, padx=10, pady=10)
        self.project = project
        self.parent = parent
        self.progress = ProgressFrame(self)
        chars = ["I", "D", "T", "E", "F"]
        self.dfa = SampleState(self)
        func = lambda c: lambda: self.dfa.next(c)
        for i in range(5):
            self.progress.buttons[i]['command'] = func(chars[i])
        self.progress.set(Prog.INFO)
        self.build()


    def set_state(self, state):
        data = state.split("_")
        if len(data) == 2:
            state = Prog.from_string(data[0])
        else:
            state = Prog.from_string(state)
        print("SET STATE {}".format(state))
        self.progress.set(state)

    def build(self):
        self.progress.pack()
        Button(self, text="NEXT", command=lambda: self.dfa.next("N")).pack()
