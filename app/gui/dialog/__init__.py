
from tkinter import messagebox, filedialog, Toplevel

from os import getcwd


def no_file_warning(file):
    """Warn if the given file path does not exist"""
    messagebox.showwarning("Not Found", file + " could not be opened")


def ask_save():
    """Ask the user to save"""
    return messagebox.askyesnocancel("Save?", "Would you like to save your work?")


def ask_project_dir(initdir=getcwd()):
    """Ask for a directory that represents an RSGrapher project"""
    return filedialog.askdirectory(title="Open Project", initialdir=initdir)

class BaseDialogWindow(Toplevel):
    """A Base class for all complex dialogs to inherit from.
       provides a dictionary to populate with information to
       return to the main application."""
    def __init__(self, root):
        super().__init__(master=root)
        self.root = root
        self.ret = {}

    def ret_update(self, **kwargs):
        """Update the return dictionary with the keyword arguments"""
        for k, v in kwargs.items():
            self.ret[k] = v

    def ret_remove(self, *args):
        """Remove key,value pairs from the return dictionary"""
        for k in args:
            del self.ret[k]

    def run(self):
        """Open this window and grab all event handlers until it closes"""
        self.grab_set()
        self.root.wait_window(self)
        return self.ret