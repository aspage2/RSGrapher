from tkinter import *

from app.gui import PANEL_BG
from app.gui.plot_frame import PlotFrame
from app.util.plotter import EmptyPlotter
from app.util.plotter.raw_plotter import RawPlotter

RADIO_BUTTON_STUFF = (("Plot Style 1", 1, lambda s, p: lambda: print("WHAT")),
                      ("Plot Style 2", 2, lambda s, p: lambda: print("WHO")),
                      ("Plot Style 3", 3, lambda s, p: lambda: print("WHEN")),
                      ("Plot Style 4", 4, lambda s, p: lambda: print("WHERE")),
                      ("Plot Style 5", 5, lambda s, p: lambda: print("WHY")))


class MainFrame(Frame):
    """Root frame of an RSGrapher application window.
       the direct child of the housing Tk instance."""

    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.project = None
        self.parent = parent
        self.currsample = None
        self.plotframe = PlotFrame(self)
        self.controlframe = Frame(self, relief=SUNKEN, border=2, bg=PANEL_BG)
        self.samplelist = Listbox(self.controlframe, width=30)
        self.radiobuttons = []
        self.plotvar = IntVar(self)
        self.build()

    def build(self):
        """Build the user interface"""
        Label(self.controlframe, text="Samples", bg=PANEL_BG).pack(anchor=N)
        self.samplelist.pack(anchor=N)
        Button(self.controlframe, text="Set Sample", command=self.set_sample, width=30).pack(anchor=N)
        Label(self.controlframe, text="Plot Types", bg=PANEL_BG).pack(anchor=N)

        for name, num, func in RADIO_BUTTON_STUFF:
            r = Radiobutton(self.controlframe, state=DISABLED, variable=self.plotvar, value=num,
                            command=func(self.currsample, self.plotframe), text=name, bg=PANEL_BG)
            r.pack(anchor=N + W)
            self.radiobuttons.append(r)

        self.controlframe.pack(side=LEFT, fill=Y)
        self.plotframe.pack(side=LEFT)

    def set_sample(self):
        """Find the highlighted element in the Listbox and give it to the plot"""
        name = self.samplelist.get(self.samplelist.curselection())
        for s in self.project.samples:
            if s.name == name:
                self.currsample = s
                self.set_default_plotter(s)

    def set_button_state(self, state):
        for r in self.radiobuttons:
            r.config(state=state)

    def refresh_project_info(self):
        """Update the GUI to reflect changes in
           project information (extraneous info)"""
        pass

    def set_project(self, project):
        """Set the project in this window"""
        self.project = project
        self.samplelist.delete(0, END)
        if project:
            for s in project.samples:
                self.samplelist.insert(END, s.name)
            if len(project.samples) == 0:
                self.plotframe.set_plotter(None)
                self.set_button_state(DISABLED)
            else:
                self.currsample = self.project.samples[0]
                self.set_default_plotter(self.currsample)
                self.set_button_state(NORMAL)
        else:
            # No project: wipe out plot and disable controls
            self.plotframe.set_plotter(None)
            self.set_button_state(DISABLED)

    def set_default_plotter(self, sample):
        self.plotframe.set_plotter(RawPlotter(sample,self.plotframe))
