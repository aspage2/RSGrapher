from tkinter import Entry, W, messagebox, Button, Label, filedialog, Text, END
from os import getcwd

from app.project.datastructure import create_project

from app.gui.dialog import BaseDialogWindow


class NewProjectPrompt(BaseDialogWindow):
    """A prompt window for creating a new project"""

    def __init__(self, root):
        super().__init__(root)
        self.title_en = Entry(self)
        self.version_en = Entry(self)
        self.description_en = Text(self, height=4, width=30)
        self.directory_en = Entry(self)

        self.build()

    def build(self):
        """Build the interface"""
        Label(self, text="Title").grid(row=0, column=0, sticky=W)
        self.title_en.grid(row=0, column=1, columnspan=3, sticky=W)

        Label(self, text="Project Number").grid(row=1, column=0, sticky=W)
        self.version_en.grid(row=1, column=1, columnspan=3, sticky=W)

        Label(self, text="Location").grid(row=2, column=0, sticky=W)
        self.directory_en.grid(row=2, column=1, columnspan=3, sticky=W)
        Button(self, text="Browse", command=self.get_directory_location).grid(row=2, column=5)

        Label(self, text="Description").grid(row=3, column=0, sticky=W)
        self.description_en.grid(row=3, column=1, columnspan=5)

        Button(self, text="Create", command=self.create).grid(row=4, column=2)
        Button(self, text="Cancel", command=self.destroy).grid(row=4, column=3)

    def check_for_valid_entries(self):
        """Check that required entries are filled"""
        if self.title_en.get() == "":
            messagebox.showwarning("Create Project", "The project needs a title.")
            return False
        if self.version_en.get() == "":
            messagebox.showwarning("Create Project", "The project needs a version.")
            return False
        if self.directory_en.get() == "":
            messagebox.showwarning("Create Project", "No directory is selected to save the project")
            return False
        return True

    def create(self):
        """Callback for when the user clicks 'Create'"""
        if not self.check_for_valid_entries():
            return
        self.ret_update(
            dir="{0}/RSG {1} - {2}".format(self.directory_en.get(), self.version_en.get(), self.title_en.get()))
        create_project(self.directory_en.get(), self.title_en.get(), self.version_en.get(),
                       self.description_en.get(1.0, END))
        self.destroy()

    def get_directory_location(self):
        """Open filedialog when user clicks 'Browse'"""
        dir = filedialog.askdirectory(title="Select Folder", initialdir=getcwd())
        self.focus_set()
        self.directory_en.insert(0, dir)
