
from app.gui.plot.plot_canvas import PlotCanvas

class PlotTool:
    ZERO = 0
    ELASTIC_ST = 1
    ELASTIC_END = 2
    def __init__(self, plotcanvas:{PlotCanvas}):
        self.canvas = plotcanvas
        self.tool = PlotTool.ZERO
        self.zeropoint = None
        self.elasticzone = [None, None]
        self.load = None
        self.disp = None

    def set_from_data(self, ascdata):
        """Set the plot from new ASC data (no pre-set zero/elastic)"""
        self.zeropoint = 0
        self.elasticzone = [0, len(ascdata)-1]

    def set_tool(self, toolid):
        if self.load is None or self.disp is None:
            return
        if toolid == PlotTool.ZERO:
            pass
        elif toolid == PlotTool.ELASTIC_ST:
            pass
        elif toolid == PlotTool.ELASTIC_END:
            pass
        else:
            raise ValueError("Given an invalid plot tool enum")
        self.tool = toolid

    def show(self):
        self.canvas.clear_plot()
        self.canvas.clear_events()