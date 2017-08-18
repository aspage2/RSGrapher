from app.util.search import lin_nearest_neighbor


class Sample:
    """A sample of rebar from a test"""

    def __init__(self, ascdata):
        self.area = None
        self.length = None
        self.data = ascdata
        self.dirty = True

        self.test_interval = [0, len(self.data) - 1]
        self.elastic_interval = list(self.test_interval)

    def set_test_interval(self, *interval):
        """Set the test interval (index) via time values"""
        if len(interval) != 2:
            raise ValueError("Arguments do not represent a time interval.")
        d0, d1 = interval
        if d0 is None: d0 = self.data.disp[self.test_interval[0]]
        if d1 is None: d1 = self.data.disp[self.test_interval[1]]
        if d1 <= d0: # t0 must be before t1
            return

        for i in range(2):
            if interval[i] is not None:
                self.test_interval[i] = lin_nearest_neighbor(interval[i], self.data.disp)
        self.dirty = True

    def test_interval_data(self):
        i0=self.test_interval[0]
        i1=self.test_interval[1]
        return self.data.time[i0:i1], self.data.disp[i0:i1], self.data.load[i0:i1]

    def elastic_interval_data(self):
        i0 = self.elastic_interval[0]
        i1 = self.elastic_interval[1]
        return self.data.time[i0:i1], self.data.disp[i0:i1], self.data.load[i0:i1]

    def strain_data(self):
        time, disp, load = self.test_interval_data()
        return (disp-disp[0])/self.length * 100.0

    def stress_data(self):
        time, disp, load = self.test_interval_data()
        return (load-load[0])/self.area

    def get_test_interval(self):
        return self.data.disp[self.test_interval]

    def set_elastic_interval(self, *interval):
        """Set the test interval (index) via time values"""
        if len(interval) != 2:
            raise ValueError("Arguments do not represent a time interval.")
        l0, l1 = interval
        if l0 is None: l0 = self.data.load[self.elastic_interval[0]]
        if l1 is None: l1 = self.data.load[self.elastic_interval[1]]
        if l1 <= l0:  # t0 must be before l1
            print("PROBLEM")
            return
        # It is assumed that the time array is sorted
        for i in range(2):
            if interval[i] is not None:
                self.elastic_interval[i] = lin_nearest_neighbor(interval[i], self.data.load)
        self.dirty = True

    def get_elastic_interval(self):
        return self.data.load[self.elastic_interval]

    def set_clean(self):
        self.dirty = False

    # def as_dict(self):
    #     """Dictionary representation for serialization"""
    #     return {"name": self.name, "area": self.area, "length": self.length, "asc_dir": self.directory,
    #             'test_interval': list(self.test_interval), 'elastic_interval': list(self.elastic_interval)}
    #
    # def write_data(self):
    #     """Write my ASC data to myname.dat in my given directory"""
    #     self.data.write(self.directory + self.name + ".dat")
    #     self.dirty = False
    #
    # @staticmethod
    # def from_dict(**info):
    #     """Create a sample instance from a dictionary representation"""
    #     data = ASCData.open(info['asc_dir'] + info['name'] + ".dat", header=False)
    #     ret = Sample(info['name'], info['area'], info['length'], data, info['asc_dir'])
    #     if None not in info['test_interval']:
    #         ret.test_interval = info['test_interval']
    #     if None not in info['elastic_interval']:
    #         ret.elastic_interval = info['elastic_interval']
    #     ret.dirty = False
    #     return ret
