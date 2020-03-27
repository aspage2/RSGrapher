from app.gui.dialog.newproject import NewProjectPrompt
from app.gui.dialog.date_input import DateInputDialog

import datetime

from tkinter import messagebox, filedialog

from app.gui.dialog.select_sample import SelectSampleDialog
from app.project.project_dir import ProjectDirectory

import os


class ProjectHandler:
    """Owns the application model and provides interface methods for modifying it"""

    def __init__(self, app, project=None):
        self.project = None
        self.curr_sample = None
        if project is not None:
            self.set_project(project)
        self._app = app

    def new_project(self):
        """Create new project"""
        self.close_project()
        info = NewProjectPrompt(self._app).run()
        if info["cancelled"]:
            return
        self.set_project(
            ProjectDirectory.create_project(
                info["title"], info["num"], info["dir"] + "/", datetime.datetime.now()
            )
        )
        self.project.write_project()
        self.cleanup_project_dir()
        self._app.content_update()

    def open_project(self):
        """Open existing project"""
        root = filedialog.askdirectory(title="Open Project")
        if root == "":
            return
        try:
            p = ProjectDirectory.open_project(root + "/")
        except IOError as e:
            messagebox.showwarning(
                title="Bad Directory",
                message="{} does not have a project.json".format(root),
            )
        else:
            self.close_project()
            self.set_project(p)
            self._app.content_update()

    def edit_info(self):
        """Edit the info of the open project"""
        pass

    def new_sample(self):
        """Add a new sample to the existing project"""
        self.project.add_blank_sample()
        s = self.project.samples[-1]
        if self.curr_sample is not None:
            s.titles = list(self.curr_sample.titles)
            s.length = self.curr_sample.length
            s.area = self.curr_sample.area
            s.precision = self.curr_sample.precision
            s.plotrange = list(self.curr_sample.plotrange)
        self.curr_sample = s
        self._app.content_update()

    def select_sample(self):
        """Set the current sample to a previously made one"""
        ret = SelectSampleDialog(
            self._app, self.project.samples, self.curr_sample
        ).run()
        if ret["cancelled"]:
            return
        self.curr_sample = self.project.samples[ret["sample"]]
        self._app.content_update()

    def delete_curr_sample(self):
        """Delete the currently open sample"""
        if self.curr_sample is not None:
            if not messagebox.askyesno(
                "Delete Sample", "Deleting Sample {}?".format(self.curr_sample.num)
            ):
                return
            self.project.samples.remove(self.curr_sample)
            if len(self.project.samples) != 0:
                self.curr_sample = self.project.samples[-1]
            self._app.content_update()

    def close_project(self):
        """Close current project"""
        if self.project is not None:
            self.project.write_project()
            self.project = None
            self.curr_sample = None

    def set_project(self, project):
        """Set project to new project"""
        self.project = project
        if self.project.has_samples:
            self.curr_sample = self.project.samples[0]
        else:
            self.curr_sample = None

    def set_date(self):
        """Set project date"""
        res = DateInputDialog(self._app).run()
        if res["cancelled"]:
            return
        self.project.set_date(res["date"])

    def cleanup_project_dir(self):
        """Move ASC files from root directory to the Raw Data folder in the project"""
        contents = os.listdir(self.project.root)
        num = 0
        for name in contents:
            if name.lower().endswith(".asc"):
                os.rename(self.project.root + name, self.project.data_dir + name)
                num += 1

        if num > 0:
            messagebox.showinfo(
                "New Project",
                "{} ASC files were moved to {}".format(num, self.project.data_dir),
            )
