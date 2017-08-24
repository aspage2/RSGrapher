
from tkinter import *

from app.gui.main_frame import MainFrame
from app.project.sample import Sample

if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x800+300+300")
    s = Sample()
    MainFrame(root, s).pack(fill=BOTH)
    root.mainloop()