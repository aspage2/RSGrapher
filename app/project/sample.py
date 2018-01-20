from app.util.asc_data import ASCData
import numpy as np


class Sample(ASCData):
    """Data for a specific sample"""

    def __init__(self, area=None, length=None, titles=None, plotrange=None):
        super().__init__()
        # Data to be written to JSON
        self._data_path = None  # Path to ASC
        self.area = area  # cross-sectional area
        self.length = length  # Pull length
        self.num = None  # Sample Number
        self.titles = titles if titles is not None else [None, None, None]  # Titles for graph output
        self._cutoff_pct = 0.1  # All data after and below 1 - pct of peak load is cut off
        self._elastic_interval = [None, None]  # Elastic interval as INDICES
        self._zero_ind = 0  # Zero point
        self.plotrange = [None, None]  # Graph plotting range as specified by the user.

        self._peak_load_ind = None
        self._cutoff_ind = None  # Index of first point cut from the end of the data.

    @property
    def elastic_zone(self):
        return self._elastic_interval

    def set_data_from_file(self, data_path):
        self.set_data(*ASCData.from_file(data_path))
        self._data_path = data_path

    def set_elastic_zone(self, L0, L1):
        """Set the elastic zone to [L0, L1]"""
        if L0 >= L1:
            raise ValueError("elastic zone is backwards")
        for i, L in enumerate((L0, L1)):
            j = self._zero_ind
            while j < len(self.load) and self.load[j] < L:
                j += 1
            if j != len(self.load):
                self._elastic_interval[i] = j

    def set_zero(self, t):
        self._zero_ind = np.argmin(np.abs(self.time - t))

    @property
    def cutoff_pct(self):
        """The percent below peak load for which to cutoff data after peak load is achieved"""
        return self._cutoff_pct

    @cutoff_pct.setter
    def cutoff_pct(self, pct):
        """Set new percent and recalculate the cutoff point"""
        self._cutoff_pct = pct
        if self.load is None:
            return
        i = self._peak_load_ind
        while i < len(self.load) and self.load[i] > self.load[self._peak_load_ind] * (1 - self._cutoff_pct):
            i += 1
        self._cutoff_ind = i

    @property
    def cutoff(self):
        return self._cutoff_ind

    @property
    def zero(self):
        return self._zero_ind

    @property
    def json(self):
        data = {'number': self.num, 'area': self.area, 'length': self.length, 'cutoff_pct': self._cutoff_pct,
                'zero_ind': self._zero_ind, 'elastic_zone': self._elastic_interval, 'data_path': self._data_path,
                'titles': self.titles, 'plot_range': self.plotrange}
        return data

    @staticmethod
    def from_json(data):
        ret = Sample()
        path = data['data_path']
        if path is not None:
            ret.set_data(*ASCData.from_file(path))

        ret.num = data['number']
        ret.area = data['area']
        ret.length = data['length']

        ret.cutoff_pct = data['cutoff_pct']
        ret._elastic_interval = data['elastic_zone']
        ret._data_path = data["data_path"]
        ret._zero_ind = data['zero_ind']

        ret.titles = data['titles']
        ret.plotrange = data["plot_range"]

        return ret
