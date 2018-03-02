
from tkinter import *
from tkinter import messagebox

from app.gui.frame.data_frame import DataFrame
from app.gui.frame.elasticintervalframe import ElasticIntervalFrame
from app.gui.frame.finalplotframe import FinalPlotFrame
from app.gui.frame.info_frame import InfoFrame
from app.gui.frame.zeroframe import ZeroFrame
from app.gui.progress_buttons import ProgressFrame


class SampleEditFrame(Frame):
    """Root frame of an RSGrapher application window.
    Provides mechanism for switching between pages for
    editing the info of a sample"""

    def __init__(self, parent, handler):
        super().__init__(parent, padx=10, pady=10)
        self.parent = parent
        self.curr_frame = None # Current edit frame to be displayed
        self._project_handler = handler # See app.project.project_handler.ProjectHandler
        self._recent_root = None # Hold most recent project directory to detect a project change

        # Make the edit page y-scrollable
        self.framecanvas = Canvas(self,width=1100,height=800)
        self.framecanvas.pack_propagate(False)
        self.scrollbar = Scrollbar(self)
        self.framecanvas['yscrollcommand'] = self.scrollbar.set
        self.scrollbar['command'] = self.framecanvas.yview
        self.frameholder = Frame(self.framecanvas)
        self.frameholder.bind("<Configure>", self.on_canvas_configure)
        self.framecanvas.create_window((self.framecanvas.winfo_width()/2, 0),
                                       window=self.frameholder, anchor=CENTER, tags="window")

        # Edit frames
        self.frames = (InfoFrame(self.frameholder, handler, self.next_frame),
                       DataFrame(self.frameholder, handler, self.next_frame),
                       ZeroFrame(self.frameholder, handler, self.next_frame),
                       ElasticIntervalFrame(self.frameholder, handler, self.next_frame),
                       FinalPlotFrame(self.frameholder, handler, self.next_frame))

        self.progress_frame = ProgressFrame(self, map(lambda f: f.title, self.frames))

        self.build()

    def content_update(self):
        """Reflect changes in the current sample (or lack thereof).
        Call propagates downward to the visible editing frame"""
        p = self._project_handler.project
        if self._recent_root != p.root: # New Project, go to infoframe
            self.set_frame(0)
            self.progress_frame.set(0, False)
        else:
            self.set_frame(1)
            self.progress_frame.set(1, False)

        self._recent_root = p.root

    def build(self):
        """Assemble the rigid components"""
        self.progress_frame.pack()
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.framecanvas.pack(fill=BOTH, expand=True)

    def set_frame(self, i):
        """Set the frame to the given index"""
        if not self.frames[i].can_update():
            return
        if self.curr_frame is not None:
            self.frames[self.curr_frame].pack_forget()
        self.curr_frame = i
        self.frames[self.curr_frame].content_update()
        self.frames[self.curr_frame].pack(fill=X)

    def next_frame(self):
        """The next frame in the lineup"""
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

    def on_canvas_configure(self,x):
        self.framecanvas.configure(scrollregion=self.framecanvas.bbox('all'))