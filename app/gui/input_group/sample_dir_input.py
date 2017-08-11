
from tkinter import *
from tkinter import filedialog

from app.gui import PANEL_BG


class SampleDirectoryInputGroup(Frame):
    def __init__(self, parent, bg=PANEL_BG, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.sample_dir = Entry(self,width=30)
        Label(self, text="ASC File ",bg=bg).pack(side=LEFT)
        self.sample_dir.pack(side=LEFT)
        Button(self, text="Browse", command=self.browse).pack(side=LEFT)

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