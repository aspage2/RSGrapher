from app.gui.plot import ELASTIC_STYLE
from app.gui.plot import POINTSTYLE, BBOX
from app.gui.plot.plotrangeframe import PlotRangeFrame
from app.util.auto_elastic import get_yield_line, line_intersection
from app.util.search import lin_max


class UTSFrame(PlotRangeFrame):
    def __init__(self, parent, sample):
        super().__init__(parent, sample)

    def init(self):
        self.canvas.set_labels("Stress vs. Strain", "Strain (% Length)", "Stress (psi)")
        stress = self.sample.stress_data()
        strain = self.sample.strain_data()
        self.canvas.set_data(strain, stress)

        i = lin_max(stress)
        self.canvas.plot(strain[i], stress[i], **POINTSTYLE)
        self.canvas.axes.text(strain[i] * 1.05, stress[i] * 1.05,
                                "Ultimate Tensile Strength: {:.2f} ksi".format(stress[i] / 1000.0), bbox=BBOX,
                                va="bottom", ha="center")

        i0, i1 = self.sample.elastic_interval
        m, b, r = get_yield_line(strain[i0:i1], stress[i0:i1], self.sample.length)
        self.canvas.plot(strain, (strain * m + b), **ELASTIC_STYLE)
        i = line_intersection(strain, stress, m, b)
        self.canvas.plot(strain[i], stress[i], **POINTSTYLE)
        self.canvas.axes.text(strain[i] * 1.05, stress[i] * 0.95,
                                "Yield Strength: {:.2f} ksi".format(stress[i] / 1000.0), bbox=BBOX, va="top", ha="left")

        xr = 1.3*max(strain)
        yr = 1.3*max(stress)
        self.canvas.set_xrange(0, xr)
        self.xrange.insert(0, str(xr))
        self.yrange.insert(0, str(yr))
        self.canvas.set_yrange(0, yr)

        self.canvas.figure.tight_layout()
        self.canvas.show()