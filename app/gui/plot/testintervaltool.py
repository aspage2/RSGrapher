
from app.gui.plot.plot_tool import PlotTool


class TestIntervalTool(PlotTool):
    """Set the test interval for the given data"""
    def __init__(self, canvas, nav, label):
        super().__init__(canvas, nav, label)

    def show(self):
        super().show()
        self.canvas.set_xrange(0, 1.3*self.canvas.xmax)
        self.canvas.set_yrange(0, 1.3*self.canvas.ymax)
        self.canvas.show()

    def setinterval(self, t0, t1):
        self.sample.set_test_interval(t0,t1)

    def getinterval(self):
        return self.sample.get_test_interval()

    def getcoord(self, event):
        return event.xdata

    def getline(self, t):
        return [t,t], [0, 1.5*self.canvas.ymax]

    def getlabeltext(self):
        return "Test Interval [{}, {}]".format(*self.sample.get_test_interval())