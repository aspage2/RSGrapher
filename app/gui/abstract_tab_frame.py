
from tkinter import *

class AbstractTabFrame(Frame):
    """Parent class for changing parts of a sample's information"""
    def __init__(self, parent, title, proj_ptr, next_frame):
        super().__init__(parent)
        self._parent = parent
        self._title = title
        self._proj_handle = proj_ptr
        self._next_frame = next_frame

    def is_done(self):
        """True if the fields needed are correct"""
        return True

    def content_update(self):
        """Called when a frame is loaded or a change occurs in the project folder"""
        raise NotImplementedError("Children of StateFrame must implement update()")

    def unload(self):
        """Called on the current frame when swapping frames out"""
        pass

    @property
    def title(self):
        return self._title

    def on_next(self):
        """Pass this method to 'next' buttons on the frame"""
        if self.is_done():
            self._next_frame()
