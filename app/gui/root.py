from tkinter import Menu, BOTH, Tk, messagebox
from app.gui.main_frame import MainFrame
from app.project.helper import Helper

class ApplicationWindow(Tk):
    """A running instance of the RSGrapher application"""

    def __init__(self, project):
        super().__init__()
        self.title("RSGrapher")
        self.main = MainFrame(self, project)
        self.helper = Helper(project,self.main)
       # self.bind_menu_actions()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.main.pack(fill=BOTH)

    def on_close(self):
        if not self.helper.try_save_open_project():
            self.destroy()

    def bind_menu_actions(self):
        """Create menu bar"""
        menubar = Menu(self)
        self.config(menu=menubar)

        # File menu
        filemenu = Menu(menubar, tearoff=False)
        filemenu.add_command(label="New Project", command=self.helper.new)
        filemenu.add_command(label="Open Project", command=self.helper.open)
        filemenu.add_command(label="Save Project", command=self.helper.save)
        filemenu.add_separator()
        filemenu.add_command(label="Export Graphs", command=self.helper.export)
        filemenu.add_separator()
        filemenu.add_command(label="Close Project", command=self.helper.close)
        filemenu.add_command(label="Quit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Project Menu
        projectmenu = Menu(menubar, tearoff=False)
        projectmenu.add_command(label='Add Sample', command=self.helper.add_sample)
        projectmenu.add_command(label='Delete Sample', command=self.helper.delete_sample)
        projectmenu.add_command(label='Add Photo to Sample', command=self.helper.noimp)
        menubar.add_cascade(label="Project", menu=projectmenu)

    def exit(self):
        self.destroy()

    def run(self):
        """Run this application"""
        self.mainloop()
