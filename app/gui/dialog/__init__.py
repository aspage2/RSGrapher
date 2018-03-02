
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
    """Base class for more custom dialogs. Provides
    logic for passing values back to main application.
    Inheritors define the layout and update return values
    with inherited methods."""
    def __init__(self, root, title="", **kwargs):
        super().__init__(master=root, **kwargs)
        self.root = root
        x = root.winfo_x()
        y = root.winfo_y()
        self.geometry("+{}+{}".format(int(x*1.25)+100, int(y*1.25)+100))
        self.title(title)
        self.resizable(0,0)

        # Keep a list of return parameters
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
        """Open this dialog. lock the main window until this one is destroyed.
        :return Dictionary of values set by user."""
        self.grab_set()
        self.root.wait_window(self)
        return self.ret