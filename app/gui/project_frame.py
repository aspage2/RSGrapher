from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import *

import matplotlib

matplotlib.use("TkAgg")

"""
Main Application Window

Subclass of a Tk.Frame to hold the project tools
"""


class ProjectFrame(Frame):
    """The frame holding the project controls, provides handles for modifying project details"""
    GRAPH_SPACE_RATIO = 0.1

    def __init__(self, parent, project=None):
        super().__init__(parent)
        self.project = project
        self.parent = parent
        self.build()
        self.refresh()
        self.pack(fill=BOTH)

    def build(self):
        """Build the User interface"""
        # Left frame to hold sample information
        infoframe = Frame(self)

        # Sample Choosing button
        Button(infoframe, text="-- Samples --", width=30).pack()

        # Sample Image thumbnail
        self.sampleimage = Canvas(infoframe, width=256, height=256, bg="grey")
        self.sampleimage.pack()

        # Sample detail window
        self.proj_title = Label(infoframe, width=30, text="")
        self.proj_title.pack()

        self.proj_descrip = Label(infoframe, width=30, text="")
        self.proj_descrip.pack()

        infoframe.pack(side=LEFT, expand=False, padx=10, pady=10)

        self.sampleframe = SampleFrame(self)
        self.sampleframe.pack(side=LEFT, expand=True)

    def refresh(self):
        if self.project.dir is None:
            self.proj_descrip.config(text="")
            self.proj_title.config(text="")
            self.sampleframe.set_sample(None)
        else:
            self.proj_descrip.config(text=self.project.desc)
            self.proj_title.config(text=self.project.title)
            self.sampleframe.set_sample(self.project.curr_sample)


class SampleFrame(Frame):
    """Notebook Frame to show data for a sample for the given project"""

    def __init__(self, parent, sample=None):
        super().__init__(parent)
        self.sample = sample
        self.pack(fill=BOTH)
        self.build()

    def set_sample(self, sample):
        self.sample=sample
        if self.sample is not None:
            self.p.plot(sample.get_disp_data(), sample.get_load_data())
            self.canvas.show()

    def build(self):
        f = Figure(figsize=(5, 5), dpi=100)
        self.p = f.add_subplot(111)
        self.p.set_xlabel("Time (s)")
        self.p.set_ylabel("Displacement (in)")
        self.p.set_title("Raw Data")
        if self.sample is not None:
            self.p.plot(self.sample.get_disp_data(), self.sample.get_load_data())

        self.canvas = FigureCanvasTkAgg(f, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(fill=BOTH,expand=True)
