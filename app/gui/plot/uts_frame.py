from app.gui.plot.plot_frame import PlotFrame


class UTSFrame(PlotFrame):
    def __init__(self, parent):
        super().__init__(parent, title="Stress vs. Strain", xlabel="Strain (% Len.)", ylabel="Stress (psi)")

    def set_sample(self, sample):
        super().set_sample(sample)
        self.canvas.set_data(sample.strain_data(), sample.stress_data())
        self.canvas.show()