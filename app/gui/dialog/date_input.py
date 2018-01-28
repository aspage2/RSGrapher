
from app.gui.dialog import BaseDialogWindow

from tkinter import *

import datetime

class DateInputDialog(BaseDialogWindow):
    def __init__(self, root):
        super().__init__(root)
        f = Frame(self)
        self._dayentry = Entry(f, width=2)
        self._monthentry = Entry(f, width=2)
        self._monthentry.pack(side=LEFT)
        Label(f, text="/").pack(side=LEFT)
        self._dayentry.pack(side=LEFT)
        Label(f, text="/").pack(side=LEFT)
        self._yearentry = Entry(f, width=4)
        self._yearentry.pack(side=LEFT)
        f.pack()
        Button(self, text="Done", command=self._submit).pack()
        self.ret_update(cancelled=True)

    def _submit(self):
        d = datetime.datetime(int(self._yearentry.get()), int(self._monthentry.get()), int(self._dayentry.get()))
        self.ret_update(cancelled=False)
        self.ret_update(date=d)
        self.destroy()