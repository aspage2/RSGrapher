from tkinter import Menu, Tk, BOTH

from app import PROJECT_TITLE
from app.gui.frame.root_frame import RootFrame
from app.project.project_handler import ProjectHandler


class AppWindow(Tk):
    """Root window for RSGrapher instance."""
    def __init__(self, project=None):
        super().__init__()
        self._project_handler = ProjectHandler(self, project)
        self._main_frame = RootFrame(self, self._project_handler)
        self._main_frame.pack(fill=BOTH)

        self.bind_menu_actions()
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.title(PROJECT_TITLE)
        self.geometry("1100x800+0+0")

        self.content_update()

    def content_update(self):
        """Update to reflect project changes"""
        proj = self._project_handler.project
        cs = self._project_handler.curr_sample
        if proj is None:
            self.title(PROJECT_TITLE)
        else:
            self.title(proj.title + (" - Sample {}".format(cs.num) if cs is not None else ""))
        self._main_frame.content_update()

    def bind_menu_actions(self):
        """Create menu bar"""
        menubar = Menu(self)
        self.config(menu=menubar)

        # File menu
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="New Project", command=self._project_handler.new_project)
        filemenu.add_command(label="Open Project", command=self._project_handler.open_project)
        filemenu.add_separator()
        filemenu.add_command(label="Project Info", command=self._project_handler.edit_info)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        samplemenu = Menu(menubar, tearoff=False)
        samplemenu.add_command(label="Add Sample", command=self._project_handler.new_sample)
        samplemenu.add_command(label="Select Sample", command=self._project_handler.select_sample)
        samplemenu.add_command(label="Delete This Sample", command=self._project_handler.delete_curr_sample)
        menubar.add_cascade(label="Sample", menu=samplemenu)

        projectmenu = Menu(menubar, tearoff=False)
        projectmenu.add_command(label="Set Project Date", command=self._project_handler.set_date)
        menubar.add_cascade(label="Project", menu=projectmenu)


    def _on_destroy(self):
        self._project_handler.close_project()

    def exit(self):
        self._on_destroy()
        self.destroy()

    def run(self):
        """Run this application"""
        self.mainloop()
