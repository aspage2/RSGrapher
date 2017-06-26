from app.gui.dialog import BaseDialogWindow

from tkinter import *
from tkinter import messagebox, filedialog

from os import getcwd


class NewSampleWindow(BaseDialogWindow):
    """A dialog for adding the information for a new sample"""

    ENTRY_WIDTH = 50

    def __init__(self, root):
        super().__init__(root=root)
        self.ret_update(cancelled=True)
        self.title("New Sample")
        self.name = None
        self.diam = None
        self.data = None
        self.build()

    def build(self):
        f = Frame(self)

        self.name = Entry(f, width=self.ENTRY_WIDTH)
        Label(f, text="Name").grid()
        self.name.grid(row=0, column=1, columnspan=3, sticky=W)

        self.diam = Entry(f, width=10)
        Label(f, text="Diameter (mm)").grid()
        self.diam.grid(row=1, column=1, columnspan=3, sticky=W)

        self.data = Entry(f, width=self.ENTRY_WIDTH)
        Label(f, text="Raw Data").grid()
        self.data.grid(row=2, column=1, columnspan=2, sticky=W)
        Button(f, text="Browse", command=self.request_data_dir).grid(row=2, column=3)

        Button(f, text="Create", command=self.create).grid(row=3, column=1)
        Button(f, text="Cancel", command=self.destroy).grid(row=3, column=2)

        f.pack(fill=BOTH)

    def check_valid_entries(self):
        if self.diam.get().strip() == "":
            messagebox.showwarning(title="Create a Sample", message="The sample must have a diameter.")
        elif self.data.get() == "":
            messagebox.showwarning(title="Create a Sample", message="No ASC data was chosen for the sample.")
        else:
            return True
        return False

    def create(self):
        if not self.check_valid_entries():
            return
        self.ret_update(name=self.name.get(), diam=self.diam.get(), data_dir=self.data.get())
        self.ret_update(cancelled=False)
        self.destroy()

    def request_data_dir(self):
        dir = filedialog.askopenfilename(title="Select ASC Data", initialdir=getcwd())
        self.focus_set()
        self.data.insert(0, dir)
