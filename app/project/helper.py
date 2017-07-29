from app.gui.dialog import ask_project_dir, ask_save
from app.gui.dialog.newproject import NewProjectPrompt
from app.gui.dialog.newsample import NewSampleWindow
from app.project.sample import Sample
from app.util.asc_data import ASCData

from tkinter import messagebox, END

from app.project.project_dir import ProjectDirectory


class Helper:
    """A helper class to extract the methods needed to update the project and GUI"""

    def __init__(self, project, frame):
        self.project = project
        self.mainframe = frame

    def new(self):
        """Create a new project"""
        try:
            data = NewProjectPrompt(self.mainframe.parent).run()
        except:
            messagebox.showwarning("Internal Error", "Something bad happened.")
        else:
            if not data['cancelled']:
                self.project = ProjectDirectory.create_project(data['title'], data['num'], data['dir'])
                self.mainframe.set_project(self.project)

    def open(self, dir=None):
        """Try to open an existing project"""
        self.try_save_open_project()
        if dir is None:
            dir = ask_project_dir()
            if dir == "":
                return
        try:
            self.project = ProjectDirectory.open(dir)
        except FileNotFoundError as e:
            print(e.filename.split("/")[-1])
            if e.filename.split("/")[-1] == "project.json":
                messagebox.showwarning(title="Open Project",
                                       message=dir + " is not a valid project folder: Could not find 'project.json'")
        else:
            self.mainframe.set_project(self.project)

    def save(self):
        """Save the current project"""
        if self.project is None:
            return
        if not self.project.up_to_date():
            self.project.write()

    def close(self):
        """Close the current project"""
        if self.try_save_open_project():
            return
        self.project = None
        self.mainframe.set_project(None)

    def export(self):
        """Export the graphs of the project as PNG's"""
        self.noimp()

    def add_sample(self):
        """Add a sample to the open project"""
        if not self.project:
            messagebox.showinfo(title="Add Sample", message="There is no open project")
            return
        try:
            data = NewSampleWindow(self.mainframe.parent).run()
        except Exception as e:
            messagebox.showwarning("Internal Error", "Something bad happened.")
            print(e)
        else:
            if not data['cancelled']:
                sample = Sample(data['name'], data['diam'], data['leng'], ASCData.open(data['data_dir']),
                                self.project.sample_dir())
                self.project.samples.append(sample)
                self.mainframe.samplelist.insert(END, data['name'])

    def delete_sample(self):
        if not self.project:
            messagebox.showinfo(title="Delete Sample", message="There is no open project.")
        if self.mainframe.currsample is None:
            messagebox.showinfo(title="Delete Sample", message="There is no selected sample.")
        else:
            if messagebox.askyesno("Delete Sample", message="Delete sample {}?".format(self.mainframe.currsample.name)):
                self.project.remove_sample(self.mainframe.currsample)
                self.mainframe.remove_sample(self.mainframe.currsample)

    def noimp(self):
        """Not implemented"""
        print("This function is not yet implemented")

    def try_save_open_project(self):
        """Ask to save an open project that has been modified.
        return true if user pressed cancel, false otherwise"""
        if self.project is not None and not self.project.up_to_date():
            resp = ask_save()
            if resp is None:
                return True
            elif resp:
                self.save()
                return False
        return False
