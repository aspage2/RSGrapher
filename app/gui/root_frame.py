from tkinter import *

from app.gui.frame.sample_edit_frame import SampleEditFrame


class RootFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent, handler):
        super().__init__(parent, padx=10, pady=10)
        self._no_project_frame = NoProjectFrame(
            self, handler.new_project, handler.open_project
        )
        self._no_sample_frame = NoSampleFrame(self, handler.new_sample)
        self._sample_frame = SampleEditFrame(self, handler)
        self._project_handler = handler

        self._curr = None

    def content_update(self):
        """Update view with new content from handler"""
        if self._curr is not None:
            self._curr.pack_forget()
        if self._project_handler.project is None:
            self._no_project_frame.pack()
            self._curr = self._no_project_frame
        elif len(self._project_handler.project.samples) == 0:
            self._no_sample_frame.pack()
            self._curr = self._no_sample_frame
        else:
            self._sample_frame.pack(fill=X)
            self._sample_frame.content_update()
            self._curr = self._sample_frame


class NoProjectFrame(Frame):
    """Visible when project handler has no open project"""

    def __init__(self, parent, np, op):
        super().__init__(parent)
        Label(self, text="No Project Open").pack()
        Button(self, text="New Project", command=np).pack()
        Button(self, text="Open Project", command=op).pack()


class NoSampleFrame(Frame):
    """Visible when project has no samples"""

    def __init__(self, parent, ns):
        super().__init__(parent)
        Label(self, text="Project has no samples!").pack()
        Button(self, text="Add Sample", command=ns).pack()
