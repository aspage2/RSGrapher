
from app.util.asc_data import ASCData


class Sample:
    """A sample of rebar from a test"""
    def __init__(self, name, area, ascdata, directory):
        self.name = name
        self.area = area
        self.data = ascdata
        self.directory = directory
        self.dirty = True

        self.test_st = None
        self.test_end = None
        self.elastic_st = None
        self.elastic_end = None


    def set_test_interval(self, test_st, test_end):
        self.test_st = test_st
        self.test_end = test_end
        self.dirty = True

    def set_elastic_interval(self, elastic_st, elastic_end):
        self.elastic_end = elastic_end
        self.elastic_st = elastic_st
        self.dirty = True

    def set_clean(self):
        self.dirty = False

    def as_dict(self):
        """Dictionary representation for serialization"""
        return {"name": self.name, "area": self.area, "asc_dir": self.directory,
                'test_interval': [self.test_st, self.test_end], 'elastic_interval': [self.elastic_st, self.elastic_end]}

    def write_data(self):
        """Write my ASC data to myname.dat in my given directory"""
        self.data.write(self.directory + self.name + ".dat")

    @staticmethod
    def from_dict(**info):
        """Create a sample instance from a dictionary representation"""
        data = ASCData.open(info['asc_dir']+info['name']+".dat", header=False)
        ret = Sample(info['name'],info['area'],data,info['asc_dir'])
        ret.set_elastic_interval(*info['elastic_interval'])
        ret.set_test_interval(*info['test_interval'])
        ret.dirty = False
        return ret
