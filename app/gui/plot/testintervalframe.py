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

        self.settingzero = False
        self.zeroline = self.canvas.plot([], [], **LINESTYLE)
        self.trimdata = self.canvas.plot([], [], **TRIMSTYLE)

        self.cutoffentry = Entry(self, width=6)
        self.cutoffentry.bind("<Return>", lambda k: self.oncutoffset())
        self.build()

    def set_sample(self, sample):
        super().set_sample(sample)
        self.canvas.set_data(sample.disp, sample.load)
        if self.sample.zero is not None:
            self.set_zeroline(self.sample.disp[self.sample.zero])
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
            print("NOT A FLOAT BIIITCH")
            return

        if c > 100:
            print ("NOT A PERCENT BIIITCH")
            return

        self.sample.peak_cutoff_pct = c / 100.0
        self.set_trimdata(self.sample.disp[self.sample.cutoff:], self.sample.load[self.sample.cutoff:])
        self.canvas.show()

    def on_click(self, event):
        if not event.inaxes:
            return
        if self.nav._active == "ZOOM":
            return
        if self.settingzero:
            self.sample.zero = event.xdata
            self.set_zeroline(self.sample.disp[self.sample.zero])
            self.canvas.show()

    def build(self):
        self.canvas.pack()
        self.cutoffentry.pack(side=LEFT)
        self.nav.pack()