from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook

import matplotlib

from app.gui import GUI_FONT
from app.gui.frame.abstract_tab_frame import AbstractTabFrame
from app.gui.plotting.peakloadframe import PeakLoadFrame
from app.gui.plotting.utsframe import UTSFrame
from app.gui.plotting.yieldloadframe import YieldLoadFrame
from app.util.pdf import create_pdf, generate_sample_layer

matplotlib.use("TkAgg")


class FinalPlotFrame(AbstractTabFrame):
    """View final plots, move labels and manage footnotes"""
    def __init__(self, parent, handler, next_frame):
        super().__init__(parent, "Final Plots", handler, next_frame)
        self.canvasnotebook = Notebook(self)
        self.peakloadframe = PeakLoadFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.peakloadframe, text="Peak Load")

        self.utsframe = UTSFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.utsframe, text="Yield Stren/UTS")

        self.yieldloadframe = YieldLoadFrame(self.canvasnotebook)
        self.canvasnotebook.add(self.yieldloadframe, text="Yield Load")

        self.build()

    def can_update(self):
        s = self._proj_handle.curr_sample
        return s.is_complete

    def content_update(self):
        s = self._proj_handle.curr_sample
        self.peakloadframe.set_sample(s)
        self.utsframe.set_sample(s)
        self.yieldloadframe.set_sample(s)

    def unload(self):
        s = self._proj_handle.curr_sample
        project = self._proj_handle.project
        pdf_dir = project.pdf_dir

        info_file = "{}temp/S{}_INFO.pdf".format(pdf_dir, s.num)
        generate_sample_layer(s, info_file)

        pl_file = "{}temp/S{}_PL.pdf".format(pdf_dir, s.num)
        self.peakloadframe.canvas.figure.savefig(pl_file)
        create_pdf(info_file, project.template_file, pl_file, pdf_dir+"Sample #{} (PeakLoad).pdf".format(s.num))

        uts_file = "{}temp/S{}_UTS.pdf".format(pdf_dir, s.num)
        self.utsframe.canvas.figure.savefig(uts_file)
        create_pdf(info_file, project.template_file, uts_file, pdf_dir+"Sample #{} (UTS).pdf".format(s.num))

        yl_file = "{}temp/S{}_YL.pdf".format(pdf_dir, s.num)
        self.yieldloadframe.canvas.figure.savefig(yl_file)
        create_pdf(info_file, project.template_file, yl_file, pdf_dir+"Sample #{} (YieldLoad).pdf".format(s.num))

        messagebox.showinfo(title="Success",message="Created 3 files in {}".format(pdf_dir))


    def build(self):
        self.canvasnotebook.pack()
        Button(self, text="Generate PDFs", command=self.on_next, font=GUI_FONT).pack(side=RIGHT)
