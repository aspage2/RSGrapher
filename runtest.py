
from app.gui.root import ApplicationWindow
from app.project.project_dir import ProjectDirectory

if __name__ == "__main__":
    application = ApplicationWindow(ProjectDirectory.open("C:/Users/egapx/Desktop/RSG100 - RSGTESTPROJECT"))
    application.mainloop()