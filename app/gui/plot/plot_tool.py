
from enum import Enum, unique

from app.gui.plot import INTERVAL_LINE_STYLE


@unique
class Focus(Enum):
    """Describes the interval endpoint being focused on"""
    Lo = 0
    Hi = 1
    Neither = 2


def valid_interval(t0, t1):
    """Endpoints of a valid interval must be strictly increasing"""
    return t0 < t1


class PlotTool:
    """Base class for selecting intervals"""
    def __init__(self, canvas, nav, label):
        self.canvas = canvas
        self.label = label
        self.nav = nav
        self.sample = None
        self.lines = [self.canvas.plot([],[], visible=False, **INTERVAL_LINE_STYLE) for i in range(2)]
        self.cid = None
        self.focus = Focus.Neither

    def set_focus(self, focus):
        """Set which interval line is in focus (lower, higher, neither)"""
        if focus is self.focus:
            return
        if self.focus is not Focus.Neither:
            self.lines[self.focus.value].set_color("k")
        if focus is not Focus.Neither:
            self.lines[focus.value].set_color("r")
        self.focus = focus
        self.canvas.show()

    def set_sample(self, sample):
        """Set the sample struct being shown"""
        self.sample = sample
        interval = self.getinterval()
        for i, line in enumerate(self.lines):
            line.set_data(self.getline(interval[i]))

    def on_click(self, event):
        """On click, try to set a new interval based on mouse location"""
        if self.nav._active == "ZOOM":
            return
        if self.focus is Focus.Neither:
            return
        interval = [None, None]
        interval[self.focus.value] = self.getcoord(event)
        self.setinterval(*interval)
        self.update_lines()
        self.label.config(text=self.getlabeltext())

    def update_lines(self):
        """Redraw lines to show an updated interval"""
        interval = self.getinterval()
        for i, line in enumerate(self.lines):
            line.set_data(self.getline(interval[i]))
        self.canvas.show()

    def show(self):
        """Reveal interval lines, bind click event"""
        if self.sample is None:
            raise RuntimeError("PlotTool Show: No sample set")
        self.cid = self.canvas.mpl_connect("button_press_event", self.on_click)
        for line in self.lines:
            line.set_visible(True)
        print("SHOWING LINES ON [{},{}]".format(*self.getinterval()))
        self.label.config(text=self.getlabeltext())
        self.canvas.show()

    def hide(self):
        """Disconnect click event, hide interval lines"""
        for line in self.lines:
            line.set_visible(False)
        if self.cid is not None:
            self.canvas.mpl_disconnect(self.cid)
            self.cid = None
        self.canvas.show()

    def getcoord(self, event):
        """Get the relevant coordinate from the click event"""
        raise NotImplementedError("Child class doesn't implement PlotTool.getcoord")

    def getline(self, t):
        """Give the data for the interval lines"""
        raise NotImplementedError("Child class doesn't implement PlotTool.getline")

    def setinterval(self, t0, t1):
        """Appropriately set the interval in the sample struct"""
        raise NotImplementedError("Child class doesn't implement PlotTool.setinterval")

    def getinterval(self):
        """Get the appropriate interval from the sample struct"""
        raise NotImplementedError("Child class doesn't implement PlotTool.getinterval")

    def getlabeltext(self):
        """Get the text for the info label"""
        raise NotImplementedError("Child class doesn't implement PlotTool.getlabeltext")