from app.gui.frame.plotrangeframe import PlotRangeFrame
from app.gui import ELASTIC_STYLE, POINT_STYLE, BBOX, TRIM_STYLE, HIGHLIGHT_STYLE
from app.util.auto_elastic import line_intersection, get_yield_line

YIELDLOAD_LABEL = "yieldload"

class YieldLoadFrame(PlotRangeFrame):
    def __init__(self, parent):
        super().__init__(parent, "Load vs. Strain", annotation_id="yieldload_annotation")
        self.yieldline = self.canvas.plot("yieldline", [], [], **ELASTIC_STYLE)
        self.yieldload = self.canvas.plot("yieldloadpoint", [], [], **POINT_STYLE)
        self.yieldset = self.canvas.plot("yieldloaddata", [], [], **HIGHLIGHT_STYLE)
        self.yieldtext = self.canvas.axes.text([], [], "", bbox=BBOX, va="top", ha="left")
        self.canvas.set_labels("Load vs. Strain", "Strain (% Length)", "Load (lbs.)")

        self._handler.watch_label(YIELDLOAD_LABEL, self.yieldtext)

    def set_sample(self, sample):
        super().set_sample(sample)
        strain = (sample.disp - sample.disp[sample.zero]) / sample.length * 100.0
        load = sample.load
        self.canvas.set_data(strain[sample.zero:sample.cutoff], load[sample.zero:sample.cutoff])
        x, y = sample.plotrange
        self.canvas.set_plotrange((0, x / sample.length * 100), (0, y))

        estrain = strain[sample.elastic_zone[0]:sample.elastic_zone[1]]
        eload = load[sample.elastic_zone[0]:sample.elastic_zone[1]]
        self.yieldset.set_data(estrain, eload)
        m, b, r = get_yield_line(estrain, eload)
        self.yieldline.set_data(strain, m * strain + b)

        intersect = line_intersection(strain, load, m, b)
        self.yieldload.set_data(strain[intersect], load[intersect])

        s = "Yield Load: {:.2f} kips".format(load[intersect] / 1000.0)
        if YIELDLOAD_LABEL not in sample.labels:
            pos = (1.10 * strain[intersect], 0.90 * load[intersect])
            sample.labels[YIELDLOAD_LABEL] = {"text":s, "pos":pos}
        else:
            pos = sample.labels[YIELDLOAD_LABEL]['pos']
        self.yieldtext.set_position(pos)
        self.yieldtext.set_text(s)

        self.canvas.figure.tight_layout()
        self.canvas.show()
