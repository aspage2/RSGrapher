
from tkinter import *
from tkinter import messagebox, filedialog

from os import getcwd

from app.project.project_dir import create_project

from app.gui.dialog import BaseDialogWindow

class ChooseSampleWindow(BaseDialogWindow):
    def __init__(self, root, samples):
        super().__init__(root)
        self.ret_update(cancelled=True)
        self.lb = Listbox(self)
        for s in samples:
            self.lb.insert(END, s.name)

        self.build()

    def build(self):
        self.lb.pack(fill=BOTH)
        Button(self,text="Choose",command=self.choose).pack()
        Button(self,text="Cancel",command=self.destroy).pack()

    def choose(self):
        self.ret_update(name=self.lb.get(self.lb.curselection()))
        self.ret_update(cancelled=False)
        self.destroy()