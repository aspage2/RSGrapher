
from app.gui.dialog.newproject import NewProjectPrompt
from tkinter import messagebox, filedialog
from app.project.project_dir import ProjectDirectory


class ProjectHandler:
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
        if info['cancelled']:
            return
        self.set_project(ProjectDirectory.create_project(info['title'],info['num'],info['dir']+"/"))
        self._app.content_update()

    def open_project(self):
        """Open existing project"""
        root = filedialog.askdirectory(title="Open Project")
        if root == "":
            return
        try:
            p = ProjectDirectory.open_project(root+"/")
        except IOError as e:
            messagebox.showwarning(title="Bad Directory", message="{} does not have a project.json".format(root))
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
        self._app.content_update()

    def select_sample(self):
        """Set the current sample to a previously made one"""
        pass

    def delete_curr_sample(self):
        """Delete the currently open sample"""
        pass

    def close_project(self):
        if self.project is not None:
            self.project.write_project()
            self.project = None
            self.curr_sample = None

    def set_project(self, project):
        self.project = project
        if self.project.has_samples:
            self.curr_sample = self.project.samples[0]
        else:
            self.curr_sample = None