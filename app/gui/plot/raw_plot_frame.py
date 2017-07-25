
from app.gui.plot.plot_frame import PlotFrame


class RawPlotFrame(PlotFrame):
    """Test frame that plots the raw load vs. displacement data"""
    def __init__(self, parent):
        super().__init__(parent, title="Raw Data", xlabel="Load (lbs)", ylabel="Disp (in)")
        self.canvas.figure.tight_layout()
        self.canvas.show()

    def set_sample(self, sample):
        super().set_sample(sample)
        self.canvas.set_data(sample.data.disp, sample.data.load)
        self.canvas.show()