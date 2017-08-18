from app.gui.plot import ELASTIC_STYLE
from app.gui.plot.plot_tool import PlotTool

from app.util.auto_elastic import suggested_elastic_zone, linear_regression


class ElasticIntervalTool(PlotTool):
    def __init__(self, canvas, nav, label):
        super().__init__(canvas, nav, label)
        self.elasticline = self.canvas.plot([],[], **ELASTIC_STYLE, visible=False)

    def show(self):
        super().show()
        disp, load = self.sample.test_interval_data()[1:]
        self.canvas.set_xrange(min(disp), max(disp))
        self.canvas.set_yrange(min(load), 1.3 * max(load))
        interval = suggested_elastic_zone(disp, load)
        self.setinterval(*interval)
        self.elasticline.set_visible(True)
        self.update_lines()

    def hide(self):
        super().hide()
        self.elasticline.set_visible(False)

    def set_sample(self, sample):
        super().set_sample(sample)
        interval = suggested_elastic_zone(*sample.test_interval_data()[1:])
        self.setinterval(*interval)
        self.update_lines()

    def getcoord(self, event):
        return event.ydata

    def getline(self, t):
        return [0, 1.5*self.canvas.xmax], [t,t]

    def getinterval(self):
        return self.sample.get_elastic_interval()

    def setinterval(self, t0, t1):
        self.sample.set_elastic_interval(t0, t1)

    def update_lines(self):
        super().update_lines()
        disp, load = self.sample.elastic_interval_data()[1:]
        dtest = self.sample.test_interval_data()[1]
        m, b, r = linear_regression(disp, load)
        self.elasticline.set_data(dtest, m*dtest+b)
        self.canvas.show()

    def getlabeltext(self):
        interval = self.sample.get_elastic_interval()
        m, b, r = linear_regression(*self.sample.elastic_interval_data()[1:])
        return "Elastic Interval: [{:.0f}, {:.0f}]".format(*interval)