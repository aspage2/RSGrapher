
from app.gui.plot.plotrangeframe import PlotRangeFrame
from app.gui.plot import POINTSTYLE, BBOX
from app.util.search import lin_max


class PeakLoadFrame(PlotRangeFrame):
    def __init__(self, parent, sample):
        super().__init__(parent, sample)

    def init(self):
        self.canvas.set_labels("Load vs. Displacement", "Displacement (in.)", "Load (lbs)")
        disp, load = self.sample.test_interval_data()[1:]
        disp -= disp[0]
        load -= load[0]

        i = lin_max(load)
        self.canvas.set_data(disp, load)
        point = ([disp[i]], [load[i]])
        self.canvas.plot(*point, **POINTSTYLE)
        self.canvas.axes.text(disp[i] * 1.05, load[i] * 1.05, "Peak Load: {:.2f} kips".format(load[i] / 1000.0),
                                      bbox=BBOX, va="bottom", ha="left")

        xr = 1.3*max(disp)
        yr = 1.3*max(load)
        self.canvas.set_xrange(0, xr)
        self.canvas.set_yrange(0, yr)
        self.xrange.insert(0, str(xr))
        self.yrange.insert(0, str(yr))
        self.canvas.figure.tight_layout()
        self.canvas.show()