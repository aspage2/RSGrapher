
class Sample:
    """A sample of rebar from a test"""

    def __init__(self, num=None):
        self._data = None

        # Data to be written to JSON
        self.area = None
        self.length = None
        self.num = num
        self.titles = [None, None, None]
        self._peak_cutoff_pct = 0.1
        self.elastic_interval = [None, None]
        self._zero = None
        self.plotrange = [None, None]

        # Other useful points
        self._peak_load = None
        self._cutoff_pt = None

    def set_data(self, data):
        self._data = data

        maxval = None
        for i, v in enumerate(self.load):
            if maxval is None or maxval < v:
                maxval = v
                self._peak_load = i
        self._zero = 100
        self.peak_cutoff_pct = 0.1

    @property
    def elastic_zone(self):
        return self.elastic_interval

    def set_elastic_zone(self, l0, l1):
        test = [l0 if l0 is not None else self.load[self.elastic_interval[0]],
                l1 if l1 is not None else self.load[self.elastic_interval[1]]]
        if test[1] < test[0]:
            return
        for i, l in enumerate((l0, l1)):
            if l is None:
                continue
            j = 0
            while j < len(self.load) and self.load[j] < l:
                j += 1
            if j != len(self.load):
                self.elastic_interval[i] = j

    @property
    def peak_cutoff_pct(self):
        """The percent below peak load for which to cutoff data after peak load is achieved"""
        return self._peak_cutoff_pct

    @peak_cutoff_pct.setter
    def peak_cutoff_pct(self, pct):
        """Set new percent and recalculate the cutoff point"""
        self._peak_cutoff_pct = pct
        i = self._peak_load
        while i < len(self.load) and self.load[i] > self.load[self._peak_load] * (1 - self._peak_cutoff_pct):
            i += 1
        self._cutoff_pt = i

    @property
    def cutoff(self):
        return self._cutoff_pt

    @property
    def zero(self):
        return self._zero

    @zero.setter
    def zero(self, disp):
        i = 0
        while i < len(self.disp) and self.disp[i] < disp:
            i += 1
        if i != len(self.disp):
            self._zero = i

    @property
    def peak_load(self):
        return self._peak_load

    @property
    def load(self):
        return self._data.load

    @property
    def disp(self):
        return self._data.disp

    def write_data(self, dir):
        """Write my ASC data to myname.dat in my given directory"""
        self._data.write(dir+"S{}.dat".format(str(self.num).zfill(3)))
