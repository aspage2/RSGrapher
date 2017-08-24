from tkinter import *

from app.gui.plot.finalplotframe import FinalPlotFrame
from app.gui.progress_buttons import ProgressFrame
from app.project.sample import Sample
from app.util.sample_state import SampleState
from app.util.progress_enum import Prog
from app.gui.infoframe import InfoFrame
from app.gui.dataframe import DataFrame
from app.gui.plot.testintervalframe import TestIntervalFrame
from app.gui.plot.elasticintervalframe import ElasticIntervalFrame

class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent, project):
        super().__init__(parent, padx=10, pady=10)
        self.parent = parent
        self.project = project
        self.progress = ProgressFrame(self)
        chars = ["I", "D", "T", "E", "F"]
        self.dfa = SampleState(self)
        func = lambda c: lambda: self.dfa.next(c)
        for i in range(5):
            self.progress.buttons[i]['command'] = func(chars[i])
        self.currstate = None
        self.progress.set(Prog.INFO)
        self.frameholder = Frame(self)
        self.frames = {Prog.INFO: InfoFrame(self.frameholder, self.dfa),
                       Prog.TESTDATA: DataFrame(self.frameholder, self.dfa),
                       Prog.TESTINT: TestIntervalFrame(self.frameholder, self.dfa),
                       Prog.ELASTICINT: ElasticIntervalFrame(self.frameholder, self.dfa),
                       Prog.FINALGRAPH: FinalPlotFrame(self.frameholder, self.dfa, self.project.graph_dir)}

        self.build()
        self.sample = Sample()
        self.dfa.next("N")

    def set_state(self, state):
        if state == "END":
            self.new_sample()
            self.dfa.next("N")
            return

        data = state.split("_")
        if len(data) == 2:
            state = Prog.from_string(data[0])
        else:
            state = Prog.from_string(state)
        if self.currstate == state:
            return
        print("SET STATE {}".format(state))
        self.progress.set(state)
        if self.currstate is not None:
            self.frames[self.currstate].hide()
            self.frames[self.currstate].pack_forget()
        self.frames[state].set_sample(self.sample)
        self.frames[state].pack(fill=BOTH)

        self.currstate = state

    def build(self):
        self.progress.pack()
        self.frameholder.pack(fill=BOTH)

    def new_sample(self):
        self.sample.write_data(self.project.sample_dir)