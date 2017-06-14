
from app.gui.dialog import ask_project_dir
from app.gui.dialog.newproject import NewProjectPrompt
from app.util.ascreader import ASCData
from tkinter import filedialog

from os import getcwd

from tkinter import messagebox

class Helper:
    """A helper class to extract the methods needed to update the project and GUI"""
    def __init__(self, project, frame):
        self.project = project
        self.frame = frame

    def new(self):
        """Create a new project"""
        try:
            dir = NewProjectPrompt(self.frame.parent).run()['dir']
        except KeyError:
            messagebox.showwarning("Internal Error", "The 'open' dialog did not output the project directory.")
        except:
            messagebox.showwarning("Internal Error", "Something bad happened.")
        else:
            self.open(dir)

    def open(self, dir=None):
        """Try to open an existing project"""
        if dir is None:
            dir = ask_project_dir()
        self.project.open(dir)
        self.frame.refresh()

    def close(self):
        """Close the current project"""
        self.project.close()
        self.frame.refresh()

    def export(self):
        """Export the graphs of the project as PNG's"""
        self.noimp()

    def add_sample(self):
        """Add a sample to the open project"""
        data = ASCData(filedialog.askopenfilename(title="Select ASC Data", initialdir=getcwd()))
        self.project.add_sample(data)
        self.frame.refresh()

    def noimp(self):
        """Not implemented"""
        print("This function is not yet implemented")
