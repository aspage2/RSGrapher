from app.gui.dialog import ask_project_dir
from app.gui.dialog.newproject import NewProjectPrompt
from app.gui.dialog.newsample import NewSampleWindow
from app.util.asc_data import ASCData

from tkinter import messagebox


class Helper:
    """A helper class to extract the methods needed to update the project and GUI"""

    def __init__(self, project, frame):
        self.project = project
        self.frame = frame

    def new(self):
        """Create a new project"""
        try:
            data = NewProjectPrompt(self.frame.parent).run()
        except Exception as e:
            messagebox.showwarning("Internal Error", "Something bad happened.")
        else:
            if not data['cancelled']:
                pass

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
        data = NewSampleWindow(self.frame.parent).run()
        self.project.add_sample(ASCData(data['data_dir']),data['name'],data['diam'])
        self.project.set_sample(data['name'])
        self.frame.refresh()

    def noimp(self):
        """Not implemented"""
        print("This function is not yet implemented")
