from app.gui.plotting import ELASTIC_STYLE, TRIMSTYLE
from app.gui.plotting import POINTSTYLE, BBOX
from app.gui.plotting.plotrangeframe import PlotRangeFrame
from app.util.auto_elastic import get_yield_line, line_intersection

from tkinter import *


class UTSFrame(PlotRangeFrame):
    def __init__(self, parent):
        super().__init__(parent, "Stress vs. Strain")
        self.sample = None
        self.uts = self.canvas.plot([], [], **POINTSTYLE)
        self.uts_text = self.canvas.axes.text(0, 0, "", bbox=BBOX, va="bottom", ha="left")
        self.yield_text = self.canvas.axes.text(0, 0, "", bbox=BBOX, va="top", ha="left")
        self.yieldline = self.canvas.plot([], [], **ELASTIC_STYLE)
        self.yieldline_set = self.canvas.plot([], [], **TRIMSTYLE)
        self.yieldpoint = self.canvas.plot([], [], **POINTSTYLE)
        self.canvas.set_labels("Stress vs. Strain", "Strain (% Length)", "Stress (psi)")

    def set_sample(self, sample):
        super().set_sample(sample)
        self.sample = sample
        x, y = sample.plotrange
        self.canvas.set_xrange(0, x / sample.length * 100)
        self.canvas.set_yrange(0, y / sample.area)

        # Calculate raw stress/strain data from sample information
        stress = (sample.load - sample.load[sample.zero]) / sample.area
        strain = (sample.disp - sample.disp[sample.zero]) / sample.length * 100.0
        self.canvas.set_data(strain[sample.zero:sample.peak_load], stress[sample.zero:sample.peak_load])
        self.uts.set_data(strain[sample.peak_load], stress[sample.peak_load])
        self.uts_text.set_position((1.10 * strain[sample.peak_load], 1.10 * stress[sample.peak_load]))
        self.uts_text.set_text("UTS: {:.2f} ksi".format(stress[sample.peak_load] / 1000.0))
        estrain = strain[sample.elastic_interval[0]:sample.elastic_interval[1]]
        estress = stress[sample.elastic_interval[0]:sample.elastic_interval[1]]
        m, b, r = get_yield_line(estrain, estress, sample.length)
        self.yieldline_set.set_data(estrain, estress)
        self.yieldline.set_data(stress, m * stress + b)
        yield_ind = line_intersection(strain, stress, m, b)
        self.yieldpoint.set_data(strain[yield_ind], stress[yield_ind])
        self.yield_text.set_position((strain[yield_ind] * 1.10, stress[yield_ind] * 0.90))
        self.yield_text.set_text("Yield Strength: {:.2f} ksi".format(stress[yield_ind] / 1000.0))
        self.canvas.figure.tight_layout()
        self.canvas.show()
