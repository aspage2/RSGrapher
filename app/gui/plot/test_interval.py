from tkinter import *

from app.gui.plot.plot_frame import PlotFrame


class TestIntervalPlot(PlotFrame):
    RADIO_BUTTON_INFO = (("Don't change test boundaries", 2, lambda p: lambda: p.set_line_tracking(None)),
                         ("Set T Start", 0, lambda p: lambda: p.set_line_tracking(0)),
                         ("Set T End", 1, lambda p: lambda: p.set_line_tracking(1)))

    def __init__(self, parent):
        """Plot frame for defining the test interval of the given sample data"""
        super().__init__(parent, title="Load vs. Time", xlabel="Time (s)", ylabel="Load (lbs)")
        self.sample = None
        self.interval = [0, 100]
        self.interval_lines = [self.canvas.plot([self.interval[i]]*2, [0, self.canvas.ymax], color="k", linestyle="--") for i in range(2)]

        self.int_label = Label(self.controlframe, text="", bg="#cecece", font=("Arial", 12, "bold"))
        self.radiobuttons = []
        self.changing = None
        self.var = IntVar()
        self.var.set(2)
        for name, val, func in self.RADIO_BUTTON_INFO:
            self.radiobuttons.append(
                Radiobutton(self.controlframe, text=name, value=val, variable=self.var, command=func(self),
                            bg="#cecece"))

        self.canvas.bind_event("button_press_event", self.onmouseclick)

        self.control_panel_build()

    def onmouseclick(self, event):
        """Mouse click event handler"""
        if event.inaxes is None:
            return
        if self.changing is None:
            return
        i = [None, None]
        i[self.changing] = event.xdata
        self.set_interval(*i)
        self.canvas.show()

    def set_sample(self, sample):
        """Set the sample of this plot frame."""
        super().set_sample(sample)
        self.sample = sample
        self.canvas.set_data(sample.data.time, sample.data.load)

        self.set_interval(*sample.get_test_interval())

    def set_interval(self, t0=None, t1=None):
        if t0 is not None:
            if (t1 is None and self.interval[1] < t0) or (t1 is not None and t1 < t0):
                print("SETTING t0 > t1")
                return
            self.interval[0] = t0
            self.interval_lines[0].set_data([t0,t0],[0,self.canvas.ymax])
        if t1 is not None:
            if (t0 is None and self.interval[0] > t1) or (t0 is not None and t1 < t0):
                print("SETTING t0 > t1")
                return
            self.interval[1] = t1
            self.interval_lines[1].set_data([t1,t1],[0,self.canvas.ymax])

        self.canvas.show()
        self.update_label()
        self.sample.set_test_interval(*self.interval)

    def set_line_tracking(self, i):
        """Set the line to change the x value of"""
        if self.changing == i:
            return
        if self.changing is not None:
            self.interval_lines[self.changing].set_color('k')
        if i is not None:
            self.interval_lines[i].set_color('r')
        self.changing = i
        self.canvas.show()

    def update_label(self):
        """Write the test interval times on the GUI"""
        self.int_label.config(text="Start: {0:^8.2f}  |  End: {1:^8.2f}".format(*self.interval))

    def control_panel_build(self):
        """Build the control panel"""
        for r in self.radiobuttons:
            r.pack(side=LEFT)
        self.int_label.pack(side=RIGHT)
