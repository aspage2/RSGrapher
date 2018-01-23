
from tkinter import *
from tkinter import messagebox

from app.gui.info_frame import InfoFrame
from app.gui.data_frame import DataFrame
from app.gui.plotting.zeroframe import ZeroFrame
from app.gui.plotting.elasticintervalframe import ElasticIntervalFrame
from app.gui.plotting.finalplotframe import FinalPlotFrame

from app.gui.progress_buttons import ProgressFrame


class SampleEditFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent, handler):
        super().__init__(parent, padx=10, pady=10)
        self.parent = parent
        self.curr_frame = None
        self._project_handler = handler
        self._recent_root = None
        self.frameholder = Frame(self)
        self.frames = (InfoFrame(self.frameholder, handler, self.next_frame),
                       DataFrame(self.frameholder, handler, self.next_frame),
                       ZeroFrame(self.frameholder, handler, self.next_frame),
                       ElasticIntervalFrame(self.frameholder, handler, self.next_frame),
                       FinalPlotFrame(self.frameholder, handler.project.photo_dir, handler, self.next_frame))

        self.progress_frame = ProgressFrame(self, map(lambda f: f.title, self.frames))

        self.build()

    def content_update(self):
        p = self._project_handler.project
        if self._recent_root != p.root: # New Project, go to infoframe
            self.set_frame(0)
            self.progress_frame.set(0, False)
        else:
            self.set_frame(1)
            self.progress_frame.set(1, False)

    def build(self):
        self.progress_frame.pack()
        self.frameholder.pack(fill=BOTH)

    def set_frame(self, i):
        if not self.frames[i].can_update():
            return
        if self.curr_frame is not None:
            self.frames[self.curr_frame].pack_forget()
        self.curr_frame = i
        print("SET {}".format(i))
        self.frames[self.curr_frame].content_update()
        self.frames[self.curr_frame].pack()

    def next_frame(self):
        if self.curr_frame is not None:
            c = self.curr_frame + 1
        else:
            raise ValueError("Frame not initially set")
        if c == len(self.frames):
            if messagebox.askyesno(title="Next Sample?", message="Create another sample?"):
                self._project_handler.new_sample()
        else:
            self.set_frame(c)
            self.progress_frame.set(c,False)