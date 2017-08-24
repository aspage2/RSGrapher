
from app.gui.plot.plotrangeframe import PlotRangeFrame
from app.gui.plot import POINTSTYLE, BBOX


class PeakLoadFrame(PlotRangeFrame):
    def __init__(self, parent):
        super().__init__(parent,"Load vs. Displacement")
        self.peakpoint = self.canvas.plot([], [], **POINTSTYLE)
        self.peaktext = self.canvas.axes.text([], [], "", bbox=BBOX, va="bottom", ha="left")
        self.canvas.set_labels("Load vs. Displacement", "Displacement (in.)", "Load (lbs)")

    def set_sample(self, sample):
        super().set_sample(sample)
        disp = sample.disp - sample.disp[sample.zero]
        load = sample.load - sample.load[sample.zero]

        self.canvas.set_data(disp[sample.zero:sample.peak_load], load[sample.zero:sample.peak_load])

        x, y = sample.plotrange
        self.canvas.set_xrange(0, x)
        self.canvas.set_yrange(0, y)

        self.peakpoint.set_data(disp[sample.peak_load],load[sample.peak_load])
        self.peaktext.set_position((1.10*disp[sample.peak_load],1.10*load[sample.peak_load]))
        self.peaktext.set_text("Peak Load: {:.2f} kips".format(load[sample.peak_load]/1000.0))
        self.canvas.figure.tight_layout()
        self.canvas.show()