import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PlotCanvas(FigureCanvasTkAgg):
    """Matplotlib canvas embedded in a tkinter window."""

    def __init__(self, fig, parent):
        super().__init__(fig, parent)
        self.figure = fig
        fig.set_facecolor("#f0f0f0")
        self.axes = fig.add_subplot(111)
        self.figure.tight_layout()
        self.axes.set_title("RSG")
        self.axes.grid(color="k", linestyle="--", linewidth=0.3)
        self._plotrange = [(0, 100), (0, 100)]
        self.datacurve = self.axes.plot([], [])[0]
        self.extra_plots = {}
        self.show()

    def set_labels(self, title=None, xlabel=None, ylabel=None):
        """Set the plotting labels"""
        if title is not None:
            self.axes.set_title(title)
        if xlabel is not None:
            self.axes.set_xlabel(xlabel)
        if ylabel is not None:
            self.axes.set_ylabel(ylabel)

    def set_plotrange(self, xrange=None, yrange=None):
        if xrange is not None:
            self.axes.set_xlim(xrange)
            self._plotrange[0] = xrange
        if yrange is not None:
            self.axes.set_ylim(yrange)
            self._plotrange[1] = yrange

    @property
    def plotrange(self):
        return tuple(self._plotrange)

    def set_data(self, xdata, ydata):
        """Set the stresscurve data"""
        self.datacurve.set_data(xdata, ydata)
        self.figure.tight_layout()

    def plot(self, name, xdata, ydata, **kwargs):
        """For plotting extra information"""
        p = self.axes.plot(xdata, ydata, **kwargs)[0]
        self.extra_plots[name] = p
        return p

    def remove_plot(self, name):
        self.extra_plots[name].remove()
        del self.extra_plots[name]

    def clear_plot(self):
        for name, plot in self.extra_plots.items():
            plot.remove()
            del self.extra_plots[name]

    def hide_all_plots(self):
        for plot in self.extra_plots.values():
            plot.set_visible(False)

    def pack(self, **kwargs):
        """tk-style pack method"""
        self.get_tk_widget().pack(**kwargs)


def add_vertical_line(canvas, x, name, **plotstyle):
    """Add a vertical line to the canvas object"""
    canvas.plot(name, (x, x), canvas.plotrange[1], **plotstyle)


def set_vertical_line(canvas, x, name):
    """Set vertical line position"""
    canvas.extra_plots[name].set_xdata((x, x))


def update_vertical_plotrange(canvas, name):
    """Update plotting range to stretch vertical line across canvas"""
    canvas.extra_plots[name].set_ydata(canvas.plotrange[1])


def add_horizontal_line(canvas, y, name, **plotstyle):
    """Add a horizontal line to the canvas object"""
    canvas.plot(name, canvas.plotrange[0], (y, y), **plotstyle)


def set_horizontal_line(canvas, y, name):
    """Set horizontal line position"""
    canvas.extra_plots[name].set_ydata((y, y))


def update_horizontal_plotrange(canvas, name):
    canvas.extra_plots[name].set_xdata(canvas.plotrange[0])