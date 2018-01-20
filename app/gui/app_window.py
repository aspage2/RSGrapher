from tkinter import Menu, Tk

from app import PROJECT_TITLE
from app.gui.main_frame import MainFrame
from app.gui.project_handler import ProjectHandler

class AppWindow(Tk):
    """A running instance of the RSGrapher application"""
    def __init__(self, project=None):
        super().__init__()
        self._project_handler = ProjectHandler(self, project)
        self._main_frame = MainFrame(self, self._project_handler)
        self._main_frame.pack()

        self.bind_menu_actions()
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.title(PROJECT_TITLE)
        self.geometry("1000x800+300+300")
        self.iconbitmap("res/window_icon.ico")

        self.content_update()

    def content_update(self):
        """Update to reflect project changes. Tell MainFrame to update"""
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

    def _on_destroy(self):
        self._project_handler.close_project()

    def exit(self):
        self._on_destroy()
        self.destroy()

    def run(self):
        """Run this application"""
        self.mainloop()
