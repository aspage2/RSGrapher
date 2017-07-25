from tkinter import *
from tkinter import messagebox
import logging

from app.gui import PANEL_BG
from app.gui.plot.empty_plot_frame import EmptyPlotFrame
from app.gui.plot.raw_plot_frame import RawPlotFrame
from app.gui.plot.test_interval import TestIntervalPlot

RADIO_BUTTON_STUFF = (("Test Interval", 1, lambda m: lambda: m.set_plot_frame(1)),
                      ("Ultimate Tensile Strength", 2, lambda m: lambda: m.set_plot_frame(2)),
                      ("Yield Strength", 3, lambda m: lambda: m.set_plot_frame(3)),
                      ("Yield Load", 4, lambda m: lambda: m.set_plot_frame(4)),
                      ("Peak Load", 5, lambda m: lambda: m.set_plot_frame(5)))



class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""
    FRAME_TI = 1
    FRAME_UTS = 2
    FRAME_YS = 3
    FRAME_YL = 4
    FRAME_PL = 5
    FRAME_EMPTY = 0

    def __init__(self, parent, project = None):
        super().__init__(parent, padx=10, pady=10)
        self.project = project
        self.parent = parent
        self.currsample = None

        self.controlframe = Frame(self, relief=SUNKEN, border=2, bg=PANEL_BG)
        self.samplelist = Listbox(self.controlframe, width=30)
        self.radiobuttons = []
        self.plotvar = IntVar(self)
        self.plotvar.set(self.FRAME_EMPTY)
        self.build_control_panel()

        self.currframe = None
        self.plotframes = []
        self.init_plot_frames()

        self.set_sample(None)

        if self.project is not None:
            self.set_project(self.project)

    def build_control_panel(self):
        """Build the user interface"""
        Label(self.controlframe, text="Samples", bg=PANEL_BG).pack(anchor=N)
        self.samplelist.pack(anchor=N)
        Button(self.controlframe, text="Set Sample", command=self.setsampleclick, width=30).pack(anchor=N)
        Label(self.controlframe, text="Plot Types", bg=PANEL_BG).pack(anchor=N)

        for name, num, func in RADIO_BUTTON_STUFF:
            r = Radiobutton(self.controlframe, state=DISABLED, variable=self.plotvar, value=num,
                            command=func(self), text=name, bg=PANEL_BG)
            r.pack(anchor=N + W)
            self.radiobuttons.append(r)

        self.controlframe.pack(side=LEFT, fill=Y)

    def setsampleclick(self):
        if len(self.samplelist.curselection()) != 1:
            messagebox.showinfo("Set Sample", "A sample must be selected")
            return
        else:
            name = self.samplelist.get(self.samplelist.curselection())
            for s in self.project.samples:
                if s.name == name:
                    self.set_sample(s)
                    return


    def init_plot_frames(self):
        """Create plot frames for each of the analysis tools"""
        self.plotframes.append(EmptyPlotFrame(self))
        self.plotframes.append(TestIntervalPlot(self))
        for i in range(4):
            self.plotframes.append(RawPlotFrame(self))
        self.plotframes.append(EmptyPlotFrame(self))

    def set_plot_frame(self, frameind):
        if frameind not in range(6):
            raise ValueError("Attempt to select an invalid plotting number")

        if self.currframe is not None:
            self.plotframes[self.currframe].pack_forget()
        self.currframe = frameind
        self.plotframes[self.currframe].set_sample(self.currsample)
        self.plotframes[self.currframe].pack(side=LEFT)

    def set_button_state(self, state):
        """Enable/Disable the radio buttons on the control frame"""
        for r in self.radiobuttons:
            r.config(state=state)

    def set_project(self, project):
        """Set the project in this window"""
        self.project = project
        self.samplelist.delete(0, END)

        if project: # Given a project to fill the app with
            for s in project.samples:
                self.samplelist.insert(END, s.name) # Append sample names to the sample list
            if len(project.samples) != 0: # Display the first sample with the first plot mechanic
                self.set_sample(project.samples[0])
            else:
                self.set_sample(None)
        else: # making project "None" means displaying the closed project screen
            self.set_sample(None)

    def remove_sample(self, sample):
        """Remove a sample from the main frame"""
        if sample is None:
            logging.warning("Attempt to remove sample nil from project")
            return
        # Remove name from list
        names = self.samplelist.get(0,END)
        for i,name in enumerate(names):
            if name == sample.name:
                self.samplelist.delete(i)
        if self.currsample is sample:
            if len(self.project.samples) == 0:
                self.set_sample(None)
            else:
                self.set_sample(self.project.samples[0])

    def set_sample(self, sample):
        """Find the highlighted element in the Listbox and give it to the plot"""
        if self.currsample is sample:
            return
        self.currsample = sample
        if sample is None:
            self.set_plot_frame(self.FRAME_EMPTY)
            self.plotvar.set(self.FRAME_EMPTY)
            self.set_button_state(DISABLED)
            return
        for s in self.project.samples:
            if s is sample:
                self.set_plot_frame(self.FRAME_TI)
                self.plotvar.set(self.FRAME_TI)
                self.set_button_state(NORMAL)