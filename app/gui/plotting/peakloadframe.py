from app.gui.plotting.drag_handler import DragHandler
from app.gui.plotting.plotrangeframe import PlotRangeFrame
from app.gui.plotting import POINTSTYLE, BBOX

PEAKLOAD_LABEL = "peakload"


class PeakLoadFrame(PlotRangeFrame):
    def __init__(self, parent):
        super().__init__(parent, "Load vs. Displacement", annotation_id="peakload_annotation")
        self.peakpoint = self.canvas.plot("peakloadpoint", [], [], **POINTSTYLE)
        self.peaktext = self.canvas.axes.text([], [], "", bbox=BBOX, va="bottom", ha="left")
        self.canvas.set_labels("Load vs. Displacement", "Displacement (in.)", "Load (lbs)")
        self._handler.watch_label(PEAKLOAD_LABEL, self.peaktext)

    def set_sample(self, sample):
        super().set_sample(sample)
        disp = sample.disp - sample.disp[sample.zero]
        load = sample.load

        self.canvas.set_data(disp[sample.zero:sample.cutoff], load[sample.zero:sample.cutoff])

        x, y = sample.plotrange
        self.canvas.set_plotrange((0, x), (0, y))

        self.peakpoint.set_data(disp[sample.peak_load], load[sample.peak_load])

        s = "Peak Load: {:.2f} kips".format(load[sample.peak_load] / 1000.0)
        if 'peakload' not in sample.labels:
            pos = (1.10 * disp[sample.peak_load], 1.10 * load[sample.peak_load])
            sample.labels[PEAKLOAD_LABEL] = {"text":s, "pos":pos}
        else:
            pos = sample.labels[PEAKLOAD_LABEL]['pos']

        self.peaktext.set_position(pos)
        self.peaktext.set_text(s)

        self.canvas.figure.tight_layout()
        self.canvas.show()
