from app.gui.plotting import ELASTIC_STYLE, TRIMSTYLE
from app.gui.plotting import POINTSTYLE, BBOX
from app.gui.plotting.plotrangeframe import PlotRangeFrame
from app.util.auto_elastic import get_yield_line, line_intersection

from tkinter import *

UTS_LABEL = "utstext"
YIELDSTRENGTH_LABEL = "yieldstrengthtext"

class UTSFrame(PlotRangeFrame):
    def __init__(self, parent):
        super().__init__(parent, "Stress vs. Strain",annotation_id="uts_annotation")
        self.sample = None
        self.uts = self.canvas.plot("utspoint",[], [], **POINTSTYLE)
        self.uts_text = self.canvas.axes.text(0, 0, "", bbox=BBOX, va="bottom", ha="left")
        self.yield_text = self.canvas.axes.text(0, 0, "", bbox=BBOX, va="top", ha="left")
        self.yieldline = self.canvas.plot("yieldline", [], [], **ELASTIC_STYLE)
        self.yieldline_data = self.canvas.plot("yieldline_data", [], [], **TRIMSTYLE)
        self.yieldpoint = self.canvas.plot("yieldpoint",[], [], **POINTSTYLE)
        self.canvas.set_labels("Stress vs. Strain", "Strain (% Length)", "Stress (psi)")

        self._handler.watch_label(UTS_LABEL, self.uts_text)
        self._handler.watch_label(YIELDSTRENGTH_LABEL, self.yield_text)

    def set_sample(self, sample):
        super().set_sample(sample)
        self.sample = sample
        x, y = sample.plotrange
        self.canvas.set_plotrange((0, x / sample.length * 100),(0, y / sample.area))

        # Calculate raw stress/strain data from sample information
        stress = (sample.load) / sample.area
        strain = (sample.disp - sample.disp[sample.zero]) / sample.length * 100.0
        self.canvas.set_data(strain[sample.zero:sample.cutoff], stress[sample.zero:sample.cutoff])

        # Ultimate Tensile Strength
        self.uts.set_data(strain[sample.peak_load], stress[sample.peak_load])

        s = "UTS: {:.2f} ksi".format(stress[sample.peak_load] / 1000.0)
        if UTS_LABEL not in sample.labels:
            pos = (1.10 * strain[sample.peak_load], 1.10 * stress[sample.peak_load])
            sample.labels[UTS_LABEL] = {"text":s, "pos":pos}
        else:
            pos = sample.labels[UTS_LABEL]['pos']
        self.uts_text.set_position(pos)
        self.uts_text.set_text(s)

        # Yield Strength
        estrain = strain[sample.elastic_zone[0]:sample.elastic_zone[1]]
        estress = stress[sample.elastic_zone[0]:sample.elastic_zone[1]]
        m, b, r = get_yield_line(estrain, estress)
        self.yieldline_data.set_data(estrain, estress)
        self.yieldline.set_data(stress, m * stress + b)
        yield_ind = line_intersection(strain, stress, m, b)
        self.yieldpoint.set_data(strain[yield_ind], stress[yield_ind])

        s = "Yield Strength: {:.2f} ksi".format(stress[yield_ind] / 1000.0)
        if YIELDSTRENGTH_LABEL not in sample.labels:
            pos = (strain[yield_ind] * 1.10, stress[yield_ind] * 0.90)
            sample.labels[YIELDSTRENGTH_LABEL] = {"text":s, "pos":pos}
        else:
            pos = sample.labels[YIELDSTRENGTH_LABEL]['pos']
        self.yield_text.set_position(pos)
        self.yield_text.set_text(s)

        self.canvas.figure.tight_layout()
        self.canvas.show()
