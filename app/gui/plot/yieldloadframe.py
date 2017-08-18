from app.gui.plot import ELASTIC_STYLE, POINTSTYLE, BBOX
from app.gui.plot.plotrangeframe import PlotRangeFrame
from app.util.auto_elastic import line_intersection, get_yield_line


class YieldLoadFrame(PlotRangeFrame):
    def __init__(self, parent, sample):
        super().__init__(parent, sample)

    def init(self):
        self.canvas.set_labels("Load vs. Strain", "Strain (% Length)", "Load (lbs.)")
        strain = self.sample.strain_data()
        load = self.sample.test_interval_data()[2]
        i0, i1 = self.sample.elastic_interval
        m, b, r = get_yield_line(strain[i0:i1], load[i0:i1], self.sample.length)
        self.canvas.plot(strain, m * strain + b, **ELASTIC_STYLE)
        i = line_intersection(strain, load, m, b)
        self.canvas.plot(strain[i], load[i], **POINTSTYLE)
        self.canvas.axes.text(strain[i] * 1.05, load[i] * 0.95,
                                       "Yield Load: {:.2f} kips".format(load[i] / 1000.0), bbox=BBOX, va="top",
                                       ha="left")
        self.canvas.set_data(strain, load)
        xr = 1.3 * max(strain)
        yr = 1.3 * max(load)
        self.canvas.set_xrange(0, xr)
        self.canvas.set_yrange(0, yr)
        self.xrange.insert(0, str(xr))
        self.yrange.insert(0, str(yr))
        self.canvas.figure.tight_layout()
        self.canvas.show()