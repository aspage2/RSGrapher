from app.gui import PANEL_BG
from app.gui.plot.plot_canvas import PlotCanvas
from app.gui.stateframe import StateFrame
from app.gui.plot import LINESTYLE, TRIMSTYLE
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

from tkinter import *

class TestIntervalFrame(StateFrame):
    def __init__(self, parent, dfa):
        super().__init__(parent, dfa)
        self.canvas = PlotCanvas(Figure((7,5),dpi=100), self)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.nav = NavigationToolbar2TkAgg(self.canvas, self)
        self.canvas.set_labels("Load vs. Displacement", "Displacement (in.)", "Load (lbs.)")
        self.zeroline = self.canvas.plot([], [], **LINESTYLE)
        self.trimdata = self.canvas.plot([], [], **TRIMSTYLE)

        self.controlframe = Frame(self, borderwidth=2, relief=SUNKEN)
        self.cutoffentry = Entry(self.controlframe, font=("Helvetica", 16), width=6)
        self.cutoffentry.bind("<Return>", lambda k: self.oncutoffset())
        self.build()

    def set_sample(self, sample):
        super().set_sample(sample)
        self.canvas.set_data(sample.disp, sample.load)
        if self.sample.zero is not None:
            self.set_zeroline(self.sample.disp[self.sample.zero])
        self.cutoffentry.delete(0, END)
        self.cutoffentry.insert(0, str(self.sample.peak_cutoff_pct*100))
        self.set_trimdata(self.sample.disp[self.sample.cutoff:], self.sample.load[self.sample.cutoff:])
        self.canvas.show()

    def set_zeroline(self, x):
        self.zeroline.set_data([x,x],[0, 1.3*self.canvas.ymax])

    def set_trimdata(self, x, y):
        self.trimdata.set_data(x, y)

    def oncutoffset(self):
        try:
            c = int(self.cutoffentry.get())
        except:
            return

        if c > 100:
            return

        self.sample.peak_cutoff_pct = c / 100.0
        self.set_trimdata(self.sample.disp[self.sample.cutoff:], self.sample.load[self.sample.cutoff:])
        self.canvas.show()

    def on_click(self, event):
        if not event.inaxes:
            return
        if self.nav._active == "ZOOM":
            return
        self.sample.zero = event.xdata
        self.set_zeroline(self.sample.disp[self.sample.zero])
        self.canvas.show()

    def ondone(self):
        self.next()

    def build(self):
        self.canvas.pack()
        Label(self.controlframe, text="Post Peak Load Cutoff (%)", font=("Helvetica", 16)).pack(padx=10, side=LEFT)
        self.cutoffentry.pack(side=LEFT)
        Button(self.controlframe, text="Done", font=("Helvetica", 16), command=self.ondone).pack(side=RIGHT, padx=10, pady=10)
        self.controlframe.pack(fill=X)
        self.nav.pack()