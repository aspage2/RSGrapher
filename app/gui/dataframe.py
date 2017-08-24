from tkinter import Button

from app.gui.stateframe import StateFrame
from app.gui.input_group.sample_num_input import SampleNumberInputGroup
from app.gui.input_group.sample_dir_input import SampleDirectoryInputGroup
from app.gui.infoframe import FONT
from app.util.asc_data import ASCData


class DataFrame(StateFrame):
    def __init__(self, parent, dfa):
        super().__init__(parent, dfa)
        self.num = SampleNumberInputGroup(self, font=FONT)
        self.dir = SampleDirectoryInputGroup(self, font=FONT)

        self.num.pack(pady=15)
        self.dir.pack(pady=15)
        Button(self, font=FONT, text="Done", command=self.ondone).pack()

    def set_sample(self, sample):
        super().set_sample(sample)

    def ondone(self):
        if not self.num.entries_valid():
            print("NUM NOT VALID")
            return
        if not self.dir.entries_valid():
            print("DIR NOT VALID")
            return

        self.next()

    def hide(self):
        self.sample.num = self.num.get_num()
        self.sample.set_data(ASCData.open(self.dir.get_dir()))