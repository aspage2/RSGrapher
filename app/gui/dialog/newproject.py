from tkinter import *
from tkinter import messagebox, filedialog

from os import getcwd

from app.gui.dialog import BaseDialogWindow

"""
NEWPROJECTPROMPT Return struct:

cancelled: if the user exited the dialog with "x" or "cancel"

title: The project title
num: The project number
dir: The project parent directory
description: the project description
"""

class NewProjectPrompt(BaseDialogWindow):
    """A prompt window for creating a new project"""

    ENTRY_WIDTH = 50

    def __init__(self, root):
        super().__init__(root)
        self.ret_update(cancelled=True)
        self.title("New Project")
        self.t = None
        self.num = None
        self.dir = None
        self.build()

    def build(self):
        """Build the interface"""
        f = Frame(self)
        self.t = Entry(f, width=self.ENTRY_WIDTH)
        Label(f,text="Title").grid()
        self.t.grid(row=0,column=1,columnspan=3,sticky=W)

        self.num = Entry(f,width=6)
        Label(f, text="Project #").grid()
        self.num.grid(row=1, column=1, columnspan=3,sticky=W)

        self.dir = Entry(f, width=self.ENTRY_WIDTH)
        Label(f, text="Folder").grid()
        self.dir.grid(row=2, column=1, columnspan=2,sticky=W)
        Button(f, command=self.get_directory_location,text="Browse").grid(row=2,column=3)

        Button(f,command=self.create,text="Create").grid(column=1)
        Button(f,command=self.destroy,text="Cancel").grid(row=4,column=2)

        f.pack(fill=BOTH, ipadx=10, ipady=10)

    def check_for_valid_entries(self):
        """Check that required entries are filled"""
        if self.t.get() == "":
            messagebox.showwarning("Create Project", "The project needs a title.")
            return False
        if self.num.get() == "":
            messagebox.showwarning("Create Project", "The project needs a version.")
            return False
        if self.dir.get() == "":
            messagebox.showwarning("Create Project", "No directory is selected to save the project")
            return False
        return True

    def create(self):
        """Callback for when the user clicks 'Create'"""
        if not self.check_for_valid_entries():
            return
        self.ret_update(title=self.t.get(),num=self.num.get(),dir=self.dir.get())
        self.ret_update(cancelled=False)
        self.destroy()

    def get_directory_location(self):
        """Open filedialog when user clicks 'Browse'"""
        dir = filedialog.askdirectory(title="Select Folder", initialdir=getcwd())
        self.focus_set()
        self.dir.insert(0, dir)
