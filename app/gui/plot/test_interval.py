from tkinter import *

from matplotlib.lines import Line2D

from app.gui.plot.plot_frame import PlotFrame


class TestIntervalPlot(PlotFrame):
    RADIO_BUTTON_INFO = (("Don't change test boundaries",2,lambda p: lambda: p.set_bound(None)),
                         ("Set T Start", 0, lambda p: lambda: p.set_bound(0)),
                         ("Set T End", 1, lambda p: lambda: p.set_bound(1)))
    def __init__(self, parent):
        """Plot frame for defining the test interval of the given sample data"""
        super().__init__(parent, title="Load vs. Time", xlabel="Time (s)", ylabel="Load (lbs)")
        self.sample = None
        self.interval_lines = []
        self.interval_lines.append(self.canvas.plot([0, 0], [0, 0], color='k', linestyle='--'))
        self.interval_lines.append(self.canvas.plot([0, 0], [0, 0], color='k', linestyle='--'))
        self.radiobuttons = []
        self.changing = None
        self.var = IntVar()
        self.var.set(2)
        for name, val, func in self.RADIO_BUTTON_INFO:
            self.radiobuttons.append(Radiobutton(self.controlframe, text=name,value=val,variable=self.var,command=func(self)))

        self.canvas.bind_event("button_press_event",self.onmouseclick)

        self.control_panel_build()

    def onmouseclick(self, event):
        if self.changing is None:
            return
        interval = list(self.sample.test_interval)
        interval[self.changing] = event.xdata
        self.sample.set_test_interval(*interval)
        self.interval_lines[self.changing].set_data([interval[self.changing]]*2,[0,self.canvas.ymax])
        self.canvas.show()

    def set_sample(self, sample):
        """Set the sample of this plot frame."""
        super().set_sample(sample)
        self.sample = sample
        self.canvas.set_data(sample.data.time, sample.data.load)
        for i in range(2):
            if sample.test_interval[i] is not None:
                self.interval_lines[i].set_data([sample.test_interval[i]] * 2, [0, self.canvas.ymax])
            else:
                self.interval_lines[i].set_data([(0.25+0.5*i)*self.canvas.xmax]*2, [0, self.canvas.ymax])

        self.canvas.show()

    def set_bound(self, i):
        if self.changing == i:
            return
        if self.changing is not None:
            self.interval_lines[self.changing].set_color('k')
        if i is not None:
            self.interval_lines[i].set_color('r')
        self.changing = i
        self.canvas.show()

    def control_panel_build(self):
        for r in self.radiobuttons:
            r.pack(side=LEFT)