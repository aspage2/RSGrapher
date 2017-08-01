from app.gui.plot.plot_frame import PlotFrame


class YieldLoadFrame(PlotFrame):
    def __init__(self, parent):
        super().__init__(parent, title="Load vs. Strain", xlabel="Strain (% Len.)", ylabel="Load (lbs.)")

    def set_sample(self, sample):
        super().set_sample(sample)
        time, disp, load = sample.test_interval_data()
        self.canvas.set_data(sample.strain_data(), load)
        self.canvas.show()