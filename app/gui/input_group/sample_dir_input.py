
from tkinter import *
from tkinter import filedialog

from app.gui import PANEL_BG
from app.util.asc_data import ASCData
from app.project.sample import Sample


class SampleDirectoryInputGroup(Frame):
    def __init__(self, parent, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.sample_dir = Entry(self,width=30, font=font)
        Label(self, text="ASC File ", font=font).pack(side=LEFT)
        self.sample_dir.pack(side=LEFT)
        Button(self, text="Browse", font=font, command=self.browse).pack(side=LEFT)

    def set_dir(self, dir):
        self.sample_dir.delete(0, END)
        if dir is not None:
            self.sample_dir.insert(0, dir)

    def get_dir(self):
        return self.sample_dir.get()

    def entries_valid(self):
        if self.sample_dir.get() == "":
            return False
        try:
            open(self.sample_dir.get(), 'r')
        except:
            return False
        return True

    def browse(self):
        dir = filedialog.askopenfilename(title="Open ASC File")
        if dir is None:
            return
        self.sample_dir.insert(0,dir)