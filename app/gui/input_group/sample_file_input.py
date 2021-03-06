from tkinter import *
from tkinter import filedialog


class SampleFileInputGroup(Frame):
    """Input path to ASC file"""

    def __init__(self, parent, font, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.sample_dir = Entry(self, width=30, font=font)
        Label(self, text="ASC File ", font=font).pack(side=LEFT)
        self.sample_dir.pack(side=LEFT)
        Button(self, text="Browse", font=font, command=self.browse).pack(side=LEFT)

    def set_initialdir(self, d):
        self._initialdir = d

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
            open(self.sample_dir.get(), "r")
        except:
            return False
        return True

    def browse(self):
        dir = filedialog.askopenfilename(
            title="Open ASC File", initialdir=self._initialdir
        )
        if dir is None:
            return
        self.sample_dir.delete(0, END)
        self.sample_dir.insert(0, dir)
