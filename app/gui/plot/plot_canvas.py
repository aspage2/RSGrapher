
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotCanvas(FigureCanvasTkAgg):
    """Instance of a matplotlib canvas with self-management"""
    def __init__(self, fig, parent):
        super().__init__(fig,parent)
        self.figure = fig
        fig.set_facecolor("#f0f0f0")
        self.axes = fig.add_subplot(111)
        self.xmax = 0.0
        self.ymax = 0.0
        self.figure.tight_layout()
        self.axes.set_title("RSG")
        self.axes.grid(color="k",linestyle="--",linewidth=0.3)
        self.datacurve = self.axes.plot([],[])[0]
        self.extra_plots = []
        self.cids = []
        self.show()

    def set_labels(self, title=None, xlabel=None, ylabel=None):
        """Set the plot labels"""
        if title is not None:
            self.axes.set_title(title)
        if xlabel is not None:
            self.axes.set_xlabel(xlabel)
        if ylabel is not None:
            self.axes.set_ylabel(ylabel)

    def reset_plotrange(self):
        self.axes.set_xlim((0,self.xmax*1.3))
        self.axes.set_ylim((0,self.ymax*1.3))

    def set_xrange(self, x0, x1):
        self.axes.set_xlim((x0,x1))
        self.show()

    def set_yrange(self, y0, y1):
        self.axes.set_ylim((y0, y1))
        self.show()

    def set_data(self, xdata, ydata):
        """Set the stresscurve data"""
        if len(xdata) != 0 and len(ydata) != 0:
            self.xmax = max(xdata)
            self.ymax = max(ydata)
        self.datacurve.set_data(xdata,ydata)
        self.reset_plotrange()
        self.figure.tight_layout()

    def plot(self, xdata, ydata, **kwargs):
        """For plotting extra information"""
        p = self.axes.plot(xdata,ydata,**kwargs)[0]
        self.extra_plots.append(p)
        return p

    def remove_plot(self, p):
        self.extra_plots.remove(p)
        p.remove()
        del p

    def clear_plot(self):
        while len(self.extra_plots) != 0:
            self.extra_plots.pop().remove()

    def hide_all_plots(self):
        for plot in self.extra_plots:
            plot.set_visible(False)

    def pack(self, **kwargs):
        """tk-style pack method"""
        self.get_tk_widget().pack(**kwargs)