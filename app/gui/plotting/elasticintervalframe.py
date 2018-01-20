from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from tkinter import *

from app.gui.plotting import ELASTIC_STYLE, LINESTYLE
from app.gui.plotting.plot_canvas import PlotCanvas
from app.gui.abstract_tab_frame import AbstractTabFrame

from app.util.auto_elastic import suggested_elastic_zone, linear_regression

RADIOBUTTONS = ({"text": "Set Zone Start", "value": 0, "command": lambda f: lambda: f.setfocus(0)},
                {"text": "Set Zone End", "value": 1, "command": lambda f: lambda: f.setfocus(1)})

FONT = ("Helvetica", 16)

class ElasticIntervalFrame(AbstractTabFrame):
    def __init__(self, parent):
        super().__init__(parent, "Elastic Zone")
        self.canvas = PlotCanvas(Figure((7, 5), dpi=100), self)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.interval_lines = [self.canvas.plot([], [], **LINESTYLE) for i in "  "]
        self.elastic_line = self.canvas.plot([], [], **ELASTIC_STYLE)
        self.nav = NavigationToolbar2TkAgg(self.canvas, self)
        self.var = IntVar(self, value=0)
        self.controlframe = Frame(self, borderwidth=2, relief=SUNKEN)
        self.curr = 1
        self.radiobuttons = []
        for b in RADIOBUTTONS:
            self.radiobuttons.append(Radiobutton(self.controlframe, font=FONT, text=b['text'], value=b['value'], variable=self.var,
                                                 command=b['command'](self)))
        self.setfocus(0)
        self.canvas.set_labels("Load vs. Displacement", "Displacement (in.)", "Load (lbs.)")
        self.canvas.show()
        self.sample = None
        self.build()

    def setfocus(self, i):
        if self.curr == i:
            return
        self.interval_lines[self.curr].set_color("k")
        self.interval_lines[i].set_color("r")
        self.curr = i
        self.canvas.show()

    def set_sample(self, sample):
        super().set_sample(sample)
        load = sample.load[sample.zero:sample.cutoff] - sample.load[sample.zero]
        disp = sample.disp[sample.zero:sample.cutoff] - sample.disp[sample.zero]
        self.canvas.set_data(disp, load)
        if None in sample.elastic_zone:
            l0, l1 = suggested_elastic_zone(disp, load)
            sample.set_elastic_zone(l0, l1)
        self.update_lines()
        self.canvas.show()

    def autoelastic_click(self):
        s = self.sample
        load = s.load[s.zero:s.cutoff] - s.load[s.zero]
        disp = s.disp[s.zero:s.cutoff] - s.disp[s.zero]
        l0, l1 = suggested_elastic_zone(disp, load)
        s.set_elastic_zone(l0, l1)
        self.update_lines()
        self.canvas.show()

    def update_lines(self):
        s = self.sample
        i0, i1 = s.elastic_zone
        e_load = s.load[i0:i1] - s.load[s.zero]
        e_disp = s.disp[i0:i1] - s.disp[s.zero]
        disp = s.disp[s.zero:s.cutoff] - s.disp[s.zero]
        m, b, r = linear_regression(e_disp, e_load)
        self.elastic_line.set_data(disp, m * disp + b)
        self.interval_lines[0].set_data([0, self.canvas.xmax * 1.3], [e_load[0], e_load[0]])
        self.interval_lines[1].set_data([0, self.canvas.xmax * 1.3], [e_load[-1], e_load[-1]])

    def on_click(self, event):
        if not event.inaxes:
            return
        if self.nav._active == "ZOOM":
            return
        interval = [None, None]
        interval[self.curr] = event.ydata
        self.sample.set_elastic_zone(*interval)
        self.update_lines()
        self.canvas.show()

    def ondone(self):
        self.next()

    def build(self):
        self.canvas.pack()
        for b in self.radiobuttons:
            b.pack(side=LEFT)
        Button(self.controlframe, font=FONT, text="Auto Elastic Zone", command=self.autoelastic_click).pack(side=LEFT,padx=10, pady=10)
        Button(self.controlframe, font=FONT, text="Done", command=self.ondone).pack(side=RIGHT,padx=10)
        self.controlframe.pack(side=LEFT,fill=BOTH)
        self.nav.pack()
