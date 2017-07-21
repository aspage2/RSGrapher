from tkinter import Label, X

from app.gui import PANEL_BG


class Plotter:
    """Base class for a manager for plot devices"""

    def __init__(self, sample, plotframe):
        self.sample = sample
        self.canvas = plotframe.canvas
        self.control_panel = self.make_control_panel(plotframe.controlframe)

    def plot_init(self):
        """Initialize data, labels, extra plot lines"""
        pass

    def event_init(self):
        """Initialize event handlers"""
        pass

    def make_control_panel(self, controlframe):
        """Create and return a tk object to fit in the control panel"""
        return None

    def cleanup(self):
        """Leave no trace of this plotter"""
        self.canvas.clear_events()
        self.canvas.clear_plot()
        self.control_panel.destroy()

    def run(self):
        """Initialize stuff"""
        self.plot_init()
        self.event_init()
        self.control_panel.pack(fill=X)
        self.canvas.show()


class EmptyPlotter(Plotter):
    """Sample-less plotter with no events"""

    def __init__(self, plotframe):
        super().__init__(None, plotframe)

    def plot_init(self):
        self.canvas.set_labels(title="RSG")
        self.canvas.set_data([], [])

    def make_control_panel(self, controlframe):
        return Label(controlframe, text="  ",bg=PANEL_BG)
