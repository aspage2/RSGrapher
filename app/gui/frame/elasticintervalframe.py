from tkinter import *

import numpy as np
from app.gui import ELASTIC_STYLE, LINE_STYLE
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from app.gui.frame.abstract_tab_frame import AbstractTabFrame
from app.gui.plot_canvas import PlotCanvas
from app.util.auto_elastic import suggested_elastic_zone, linear_regression

RADIOBUTTONS = ({"text": "Set Zone Start", "value": 0, "command": lambda f: lambda: f.setfocus(0)},
                {"text": "Set Zone End", "value": 1, "command": lambda f: lambda: f.setfocus(1)})

FONT = ("Helvetica", 16)

class ElasticIntervalFrame(AbstractTabFrame):
    def __init__(self, parent, handler, next_frame):
        super().__init__(parent, "Elastic Zone", handler, next_frame)
        self.canvas = PlotCanvas(Figure((7, 5), dpi=100), self)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.interval_lines = [self.canvas.plot("interval{}".format(i), [], [], **LINE_STYLE) for i in (1, 2)]
        self.elastic_line = self.canvas.plot("elasticline", [], [], **ELASTIC_STYLE)
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

    def can_update(self):
        s = self._proj_handle.curr_sample
        return s.dir is not None

    def content_update(self):
        self.sample = self._proj_handle.curr_sample
        s = self.sample
        disp = s.disp[:s.cutoff]
        load = s.load[:s.cutoff]
        self.canvas.set_data(disp, load)
        self.canvas.set_plotrange((disp[0], 1.3*np.max(disp)),(0, 1.3*np.max(load)))
        if None in s.elastic_zone:
            l0, l1 = suggested_elastic_zone(disp, load)
            s.set_elastic_zone(l0, l1)
        self.update_lines()
        self.canvas.show()

    def autoelastic_click(self):
        s = self.sample
        load = s.load[:s.cutoff]
        disp = s.disp[:s.cutoff]
        l0, l1 = suggested_elastic_zone(disp, load)
        s.set_elastic_zone(l0, l1)
        self.update_lines()
        self.canvas.show()

    def update_lines(self):
        s = self.sample
        i0, i1 = s.elastic_zone
        e_load = s.load[i0:i1]
        e_disp = s.disp[i0:i1]
        m, b, r = linear_regression(e_disp, e_load)
        self.elastic_line.set_data(s.disp, m * s.disp + b)
        self.interval_lines[0].set_data(self.canvas.plotrange[0], [e_load[0], e_load[0]])
        self.interval_lines[1].set_data(self.canvas.plotrange[0], [e_load[-1], e_load[-1]])

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

    def build(self):
        self.canvas.pack()
        for b in self.radiobuttons:
            b.pack(side=LEFT)
        Button(self.controlframe, font=FONT, text="Auto Elastic Zone", command=self.autoelastic_click).pack(side=LEFT,padx=10, pady=10)
        Button(self.controlframe, font=FONT, text="Done", command=self.on_next).pack(side=RIGHT,padx=10)
        self.controlframe.pack(side=LEFT,fill=BOTH)
        self.nav.pack()
