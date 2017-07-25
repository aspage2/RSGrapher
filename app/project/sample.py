
from app.util.asc_data import ASCData


class Sample:
    """A sample of rebar from a test"""
    def __init__(self, name, area, length, ascdata, directory):
        self.name = name
        self.area = area
        self.length = length
        self.data = ascdata
        self.directory = directory
        self.dirty = True

        self.test_interval = (None, None)
        self.elastic_interval = (None, None)


    def set_test_interval(self, test_st, test_end):
        self.test_interval = (test_st, test_end)
        self.dirty = True

    def set_elastic_interval(self, elastic_st, elastic_end):
        self.elastic_interval = (elastic_st, elastic_end)
        self.dirty = True

    def set_clean(self):
        self.dirty = False

    def as_dict(self):
        """Dictionary representation for serialization"""
        return {"name": self.name, "area": self.area, "length": self.length, "asc_dir": self.directory,
                'test_interval': list(self.test_interval), 'elastic_interval': list(self.elastic_interval)}

    def write_data(self):
        """Write my ASC data to myname.dat in my given directory"""
        self.data.write(self.directory + self.name + ".dat")

    @staticmethod
    def from_dict(**info):
        """Create a sample instance from a dictionary representation"""
        data = ASCData.open(info['asc_dir']+info['name']+".dat", header=False)
        ret = Sample(info['name'],info['area'],info['length'],data,info['asc_dir'])
        ret.set_elastic_interval(*info['elastic_interval'])
        ret.set_test_interval(*info['test_interval'])
        ret.dirty = False
        return ret
