
from app.gui.dialog import BaseDialogWindow
from app.gui import GUI_FONT
from tkinter import *
import datetime


class DateInputDialog(BaseDialogWindow):
    """Enter the date that the testing took place on"""
    def __init__(self, root):
        super().__init__(root, "Set Date", padx=10, pady=10)
        rf = Frame(self, padx=20, pady=10)
        Label(rf, text="month/day/year", font=GUI_FONT).pack()

        f = Frame(rf)
        self._dayentry = Entry(rf, width=2, font=GUI_FONT)
        self._monthentry = Entry(rf, width=2, font=GUI_FONT)
        self._monthentry.pack(side=LEFT)
        Label(rf, text="/", font=GUI_FONT).pack(side=LEFT)
        self._dayentry.pack(side=LEFT)
        Label(rf, text="/", font=GUI_FONT).pack(side=LEFT)
        self._yearentry = Entry(rf, width=4, font=GUI_FONT)
        self._yearentry.pack(side=LEFT)
        f.pack()

        Button(rf, text="Done", command=self._submit, font=GUI_FONT).pack()
        rf.pack()

        self.ret_update(cancelled=True)

    def _submit(self):
        d = datetime.datetime(int(self._yearentry.get()), int(self._monthentry.get()), int(self._dayentry.get()))
        self.ret_update(cancelled=False)
        self.ret_update(date=d)
        self.destroy()