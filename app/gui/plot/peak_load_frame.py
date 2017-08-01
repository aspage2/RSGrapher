from app.gui.plot.plot_frame import PlotFrame


class PeakLoadFrame(PlotFrame):
    def __init__(self, parent):
        super().__init__(parent,title="Load vs. Displacement", xlabel="Displacement (in.)", ylabel="Load (lbs.)")

    def set_sample(self, sample):
        super().set_sample(sample)
        time, disp, load = sample.test_interval_data()
        self.canvas.set_data(disp, load)
        self.canvas.show()
