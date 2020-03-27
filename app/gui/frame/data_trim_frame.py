from tkinter import *

import numpy as np
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

from app.gui import LINE_STYLE, TRIM_STYLE, GUI_FONT
from app.gui.frame.abstract_tab_frame import AbstractTabFrame
from app.gui.plotting.plot_canvas import PlotCanvas


class DataTrimFrame(AbstractTabFrame):
    """Trim the data to remove extraneous data points (before/after actual test)"""
    def __init__(self, parent, handle, next_frame):
        super().__init__(parent, "Trim Data", handle, next_frame)
        self.canvas = PlotCanvas(Figure((7, 5), dpi=100), self)
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.nav = NavigationToolbar2Tk(self.canvas, self)
        self.canvas.set_labels("Load vs. Time", "Time (s)", "Load (lbs.)")
        self.zeroline = self.canvas.plot("zeroline", [], [], **LINE_STYLE)
        self.trimdata = self.canvas.plot("trimdata", [], [], **TRIM_STYLE)

        self._show_time = True

        self._cs = None
        self.controlframe = Frame(self, borderwidth=2, relief=SUNKEN)
        self.cutoffentry = Entry(self.controlframe, font=GUI_FONT, width=6)
        self.cutoffentry.bind("<Return>", lambda k: self.on_cutoff_set())
        self.zerolabel = Label(self.controlframe, text="Zero: {:0.1f} s".format(0), font=GUI_FONT)
        self.viewbutton = Button(self.controlframe, text="SHOW DISP", command=self._toggle_view)
        self.build()

    def _toggle_view(self):
        if self._cs is None:
            return
        if self._show_time:
            b = "SHOW TIME"
            z = self._cs.disp[self._cs.zero]
            t = self._cs.disp[self._cs.cutoff:]
            self.canvas.set_labels("Load vs. Displacement", "Displacement (in)")
            self.canvas.set_data(self._cs.disp, self._cs.load)
            self.canvas.set_plotrange((self._cs.disp[0], 1.3*np.max(self._cs.disp)), (0, 1.3*np.max(self._cs.load)))
        else:
            b = "SHOW DISP"
            z = self._cs.time[self._cs.zero]
            t = self._cs.time[self._cs.cutoff:]
            self.canvas.set_labels("Load vs. Time", "Time (s)")
            self.canvas.set_data(self._cs.time, self._cs.load)
            self.canvas.set_plotrange((self._cs.time[0], 1.3 * np.max(self._cs.time)), (0, 1.3 * np.max(self._cs.load)))
        self.viewbutton['text'] = b
        self._show_time = not self._show_time
        self.set_zeroline(z)
        self.set_trimdata(t,self._cs.load[self._cs.cutoff:])
        self.canvas.draw()

    def can_update(self):
        s = self._proj_handle.curr_sample
        return s.dir is not None

    def content_update(self):
        self._cs = self._proj_handle.curr_sample
        self._show_time = True
        self.canvas.set_data(self._cs.time, self._cs.load)
        self.canvas.set_plotrange((self._cs.time[0], 1.3*self._cs.time[-1]), (0,1.3*np.max(self._cs.load)))
        self.zerolabel['text'] = "Zero: {:0.1f} s".format(self._cs.time[self._cs.zero])
        self.set_zeroline(self._cs.time[self._cs.zero])
        self.cutoffentry.delete(0, END)
        self.cutoffentry.insert(0, str(self._cs.cutoff_pct * 100))
        self.set_trimdata(self._cs.time[self._cs.cutoff:], self._cs.load[self._cs.cutoff:])
        self.canvas.draw()

    def set_zeroline(self, x):
        self.zerolabel['text'] = "Zero: {:0.1f} {}".format(x, "s" if self._show_time else "in")
        self.zeroline.set_data([x, x], self.canvas.plotrange[1])

    def set_trimdata(self, x, y):
        self.trimdata.set_data(x, y)

    def on_cutoff_set(self):
        try:
            c = float(self.cutoffentry.get())
        except:
            return
        if c > 100:
            return

        self._cs.cutoff_pct = c / 100.0
        if self._show_time:
            data = self._cs.time
        else:
            data = self._cs.disp
        self.set_trimdata(data[self._cs.cutoff:], self._cs.load[self._cs.cutoff:])
        self.canvas.draw()

    def on_click(self, event):
        if not event.inaxes:
            return
        if self.nav._active == "ZOOM":
            return
        self._cs.set_zero(event.xdata)
        self.set_zeroline(event.xdata)
        self.canvas.draw()

    def is_done(self):
        try:
            f = float(self.cutoffentry.get())
        except:
            return False
        return True

    def build(self):
        self.canvas.pack()
        Label(self.controlframe, text="Post Peak Load Cutoff (%)", font=GUI_FONT).pack(padx=10, side=LEFT)
        self.cutoffentry.pack(side=LEFT)
        self.zerolabel.pack(side=LEFT, padx=10)
        self.viewbutton.pack(side=LEFT, padx=10)
        Button(self.controlframe, text="Done", font=GUI_FONT, command=self.on_next).pack(side=RIGHT, padx=10,
                                                                                                 pady=10)
        self.controlframe.pack(fill=X)
        self.nav.pack()
