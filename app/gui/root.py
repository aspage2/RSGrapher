from tkinter import Menu, BOTH, Tk, messagebox

from app.gui.dialog.newproject import NewProjectPrompt
from app.gui.main_frame import MainFrame
from app.project.project_dir import ProjectDirectory


class ApplicationWindow(Tk):
    """A running instance of the RSGrapher application"""

    def __init__(self):
        super().__init__()
        self.title("RSGrapher")
        self.geometry("1000x800+300+300")
        self.main = None
        self.bind_menu_actions()

    def bind_menu_actions(self):
        """Create menu bar"""
        menubar = Menu(self)
        self.config(menu=menubar)

        # File menu
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="New Project", command=self.new)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

    def new(self):
        if self.main is not None:
            self.main.destroy()
        data = NewProjectPrompt(self).run()
        if data['cancelled']:
            self.exit()
            return
        proj = ProjectDirectory.create_project(data['title'], data['num'], data['dir'])
        self.title("RSGrapher: {}".format(proj.title))
        self.main = MainFrame(self, proj)
        self.main.pack()

    def exit(self):
        self.destroy()

    def run(self):
        """Run this application"""
        self.mainloop()
