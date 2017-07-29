from app.util.asc_data import ASCData
from app.util.search import nearest_neighbor


class Sample:
    """A sample of rebar from a test"""

    def __init__(self, name, area, length, ascdata, directory):
        self.name = name
        self.area = area
        self.length = length
        self.data = ascdata
        self.directory = directory
        self.dirty = True

        self.test_interval = [None, None]
        self.elastic_interval = [None, None]

    def set_test_interval(self, int_st, int_end):
        self.test_interval = [nearest_neighbor(int_st, self.data.time) if int_st is not None else None,
                              nearest_neighbor(int_end, self.data.time) if int_end is not None else None]
        self.dirty = True

    def get_test_interval(self):
        return self.data.time[self.test_interval]

    def set_elastic_interval(self, elastic_st, elastic_end):
        self.elastic_interval = (elastic_st, elastic_end)
        self.dirty = True

    def get_elastic_interval(self):
        return self.elastic_interval

    def set_clean(self):
        self.dirty = False

    def as_dict(self):
        """Dictionary representation for serialization"""
        return {"name": self.name, "area": self.area, "length": self.length, "asc_dir": self.directory,
                'test_interval': list(self.get_test_interval()), 'elastic_interval': list(self.elastic_interval)}

    def write_data(self):
        """Write my ASC data to myname.dat in my given directory"""
        self.data.write(self.directory + self.name + ".dat")

    @staticmethod
    def from_dict(**info):
        """Create a sample instance from a dictionary representation"""
        data = ASCData.open(info['asc_dir'] + info['name'] + ".dat", header=False)
        ret = Sample(info['name'], info['area'], info['length'], data, info['asc_dir'])
        ret.set_elastic_interval(*info['elastic_interval'])
        ret.set_test_interval(*info['test_interval'])
        ret.dirty = False
        return ret
