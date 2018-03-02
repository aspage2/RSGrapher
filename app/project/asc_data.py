import numpy as np


class ASCData:
    def __init__(self, time=None, load=None, disp=None):
        if time is not None and load is not None and disp is not None:
            self.set_data(time, load, disp)
        else:
            self.time = None
            self.load = None
            self.disp = None
            self.len = None

    def set_data(self, time, load, disp):
        self.time = np.array(time)
        self.disp = np.array(disp)
        self.load = np.array(load)
        self.len = len(time)

    def __len__(self):
        return self.len

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (self.time[key.start:key.stop], self.disp[key.start:key.stop], self.load[key.start:key.stop])
        return (self.time[key], self.disp[key], self.load[key])

    @staticmethod
    def from_file(filename):
        time = []
        load = []
        disp = []
        with open(filename, 'r') as fh:
            for i in range(7):
                fh.readline()
            line = fh.readline().strip()
            while line != "":
                t, d, l = line.split("\t")
                time.append(float(t))
                load.append(float(l))
                disp.append(float(d))
                line = fh.readline().strip()

        return time, load, disp


