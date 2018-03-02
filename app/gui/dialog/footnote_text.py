
from app.gui.dialog import BaseDialogWindow

from tkinter import *


class FootnoteDialog(BaseDialogWindow):
    """Add/modify the footnote text on a graph"""
    def __init__(self, root, text):
        super().__init__(root, "Footnote Text")
        self._textbox = Text(self, width=30, height=5)
        self._textbox.insert("0.0", text)
        self._textbox.pack()
        self.ret_update(cancelled=True)
        Button(self, text="Done", command=self.on_done).pack()

    def on_done(self):
        self.ret_update(text=self._textbox.get("0.0", END))
        self.ret_update(cancelled=False)
        self.destroy()
