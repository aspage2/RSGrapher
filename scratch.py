
from app.gui.dialog.date_input import DateInputDialog

from tkinter import *

from app.gui.dialog.newproject import NewProjectPrompt

root = Tk()

def cmd():
    return NewProjectPrompt(root).run()

Button(root, padx=20, pady=20,text="CMD", command=cmd).pack()
root.mainloop()