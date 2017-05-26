from tkinter import filedialog
from tkinter import messagebox

from os import getcwd

def no_file_warning (file):
    messagebox.showwarning ("Not Found", file + " could not be opened")

def ask_save ():
    return messagebox.askyesnocancel ("Save?", "Would you like to save your work?")

def ask_project_dir (initdir = getcwd()):
    return filedialog.askdirectory (title="Open Project", initialdir=initdir)
