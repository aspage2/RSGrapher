
from app.util.plotter import Plotter

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg

class RawPlotter(Plotter):
    """Plot raw load vs. displacement data"""
    def __init__(self, sample, plotframe):
        super().__init__(sample,plotframe)

    def plot_init(self):
        self.canvas.set_data(self.sample.data.load, self.sample.data.disp)
        self.canvas.set_labels(title="Raw Data", xlabel="Load", ylabel="Disp")
        self.canvas.show()

    def make_control_panel(self, controlframe):
        return NavigationToolbar2TkAgg(self.canvas,controlframe)