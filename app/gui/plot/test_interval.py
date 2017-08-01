from tkinter import *

from app.gui.plot.plot_frame import PlotFrame


class TestIntervalFrame(PlotFrame):
    RADIO_BUTTON_INFO = (("Don't change test boundaries", 2, lambda p: lambda: p.set_line_tracking(None)),
                         ("Set T Start", 0, lambda p: lambda: p.set_line_tracking(0)),
                         ("Set T End", 1, lambda p: lambda: p.set_line_tracking(1)))

    def __init__(self, parent):
        """Plot frame for defining the test interval of the given sample data"""
        super().__init__(parent, title="Displacement vs. Time", xlabel="Time (s)", ylabel="Displacement (in.)")
        self.sample = None
        self.interval_lines = [self.canvas.plot([], [], color="k", linestyle="--") for i in '  ']

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
        if (event.inaxes is None or
            self.changing is None or
            self.nav._active == "ZOOM"):
            return
        i = [None, None]
        i[self.changing] = event.xdata
        self.sample.set_test_interval(*i)
        self.interval_update()

    def set_sample(self, sample):
        """Set the sample of this plot frame."""
        super().set_sample(sample)
        self.sample = sample
        self.canvas.set_data(sample.data.time, sample.data.disp)
        self.interval_update()

    def interval_update(self):
        interval = self.sample.get_test_interval()
        for i, t in enumerate(interval):
            self.interval_lines[i].set_data([t, t], [0, self.canvas.ymax])
        self.canvas.show()
        self.int_label.config(text="Start: {0:^8.2f}  |  End: {1:^8.2f}".format(*interval))

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

    def control_panel_build(self):
        """Build the control panel"""
        for r in self.radiobuttons:
            r.pack(side=LEFT)
        self.int_label.pack(side=RIGHT)
