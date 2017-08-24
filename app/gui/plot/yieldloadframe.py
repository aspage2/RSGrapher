from app.gui.plot import ELASTIC_STYLE, POINTSTYLE, BBOX, TRIMSTYLE
from app.gui.plot.plotrangeframe import PlotRangeFrame
from app.util.auto_elastic import line_intersection, get_yield_line


class YieldLoadFrame(PlotRangeFrame):
    def __init__(self, parent):
        super().__init__(parent, "Load vs. Strain")
        self.yieldline = self.canvas.plot([], [], **ELASTIC_STYLE)
        self.yieldload = self.canvas.plot([], [], **POINTSTYLE)
        self.yieldset = self.canvas.plot([], [], **TRIMSTYLE)
        self.yieldtext = self.canvas.axes.text([], [], "", bbox=BBOX, va="top", ha="left")
        self.canvas.set_labels("Load vs. Strain", "Strain (% Length)", "Load (lbs.)")
    def set_sample(self, sample):
        super().set_sample(sample)

        strain = (sample.disp - sample.disp[sample.zero]) / sample.length * 100.0
        load = sample.load - sample.load[0]
        self.canvas.set_data(strain[sample.zero:sample.cutoff], load[sample.zero:sample.cutoff])
        x, y = sample.plotrange
        self.canvas.set_xrange(0, x / sample.length * 100)
        self.canvas.set_yrange(0, y)

        estrain = strain[sample.elastic_interval[0]:sample.elastic_interval[1]]
        eload = load[sample.elastic_interval[0]:sample.elastic_interval[1]]
        self.yieldset.set_data(estrain, eload)
        m, b, r = get_yield_line(estrain, eload, sample.length)
        self.yieldline.set_data(strain, m * strain + b)

        intersect = line_intersection(strain, load, m, b)
        self.yieldload.set_data(strain[intersect], load[intersect])

        self.yieldtext.set_position((1.10 * strain[intersect], 0.90 * load[intersect]))
        self.yieldtext.set_text("Yield Load: {:.2f} kips".format(load[intersect] / 1000.0))
        self.canvas.figure.tight_layout()
        self.canvas.show()
