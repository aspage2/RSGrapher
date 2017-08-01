from app.gui.plot.plot_frame import PlotFrame
from app.util.auto_elastic import suggested_elastic_zone, get_yield_line

from tkinter import *


class ElasticIntervalFrame(PlotFrame):
    RADIO_BUTTON_INFO = (("Don't change test boundaries", 2, lambda p: lambda: p.set_line_tracking(None)),
                         ("Set Elastic Start", 0, lambda p: lambda: p.set_line_tracking(0)),
                         ("Set Elastic End", 1, lambda p: lambda: p.set_line_tracking(1)))

    def __init__(self, parent):
        super().__init__(parent, title="Load vs. Displacement", xlabel="Displacement (in.)", ylabel="Load (lbs.)")
        self.sample = None
        self.interval_lines = [self.canvas.plot([], [], color="k", linestyle="--") for i in "  "]

        self.yield_line = self.canvas.plot([], [], color="g", linewidth=1.0)
        self.radiobuttons = []
        self.changing = None
        self.var = IntVar()
        self.var.set(2)
        for name, val, func in self.RADIO_BUTTON_INFO:
            self.radiobuttons.append(
                Radiobutton(self.controlframe, text=name, value=val, variable=self.var, command=func(self),
                            bg="#cecece"))

        self.auto_button = Button(self.controlframe, text="Suggested Elastic Zone", command=self.autoelasticzone)

        self.canvas.bind_event("button_press_event", self.onmouseclick)
        self.control_panel_build()
        self.origin = [0,0]

    def autoelasticzone(self):
        self.sample.set_elastic_interval(*suggested_elastic_zone(*self.sample.test_interval_data()[1:]))
        self.update_interval()

    def set_sample(self, sample):
        super().set_sample(sample)
        self.sample = sample
        time, disp, load = sample.test_interval_data()
        self.canvas.set_data(disp, load)

        self.update_interval()

    def set_line_tracking(self, val):
        if val == self.changing:
            return
        if self.changing is not None:
            self.interval_lines[self.changing].set_color("k")
        self.changing = val
        if val is None:
            return
        self.interval_lines[val].set_color('r')
        self.canvas.show()

    def onmouseclick(self, event):
        if self.changing is None or event.inaxes is None:
            return
        interval = [None, None]
        interval[self.changing] = event.ydata
        self.sample.set_elastic_interval(*interval)
        self.update_interval()

    def control_panel_build(self):
        for r in self.radiobuttons:
            r.pack(side=LEFT)
        self.auto_button.pack(side=LEFT)

    def update_interval(self):
        if self.sample is None:
            return
        elastic_interval = self.sample.get_elastic_interval()
        for i, e in enumerate(elastic_interval):
            self.interval_lines[i].set_data([0, 100], [e, e])
        disp, load = self.sample.elastic_interval_data()[1:]
        m,b,r = get_yield_line(disp, load, self.sample.length)
        disp = self.sample.test_interval_data()[1]
        self.yield_line.set_data(disp, m*disp + b)
        self.canvas.show()
