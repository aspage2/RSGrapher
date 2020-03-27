from app.gui.dialog import BaseDialogWindow

from tkinter import *


class SelectSampleDialog(BaseDialogWindow):
    """Choose a sample to work on"""

    def __init__(self, root, samples, curr):
        super().__init__(root, "Select Sample")
        self.ret_update(cancelled=True)
        self._sample = IntVar()
        self._sample.set(samples.index(curr))
        for i, s in enumerate(samples):
            Radiobutton(
                self, text="Sample {}".format(s.num), variable=self._sample, value=i
            ).pack()
        Button(self, text="Select", command=self.done).pack()

    def done(self):
        self.ret_update(cancelled=False)
        self.ret_update(sample=self._sample.get())
        self.destroy()
