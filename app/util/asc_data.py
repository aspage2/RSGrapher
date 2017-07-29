import numpy as np


class ASCData:
    def __init__(self, time, load, disp):
        if len(time) != len(disp):
            raise ValueError("Lists are not the same length")
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

    def write(self, filename):
        with open(filename, 'w') as fh:
            for i in range(self.len):
                fh.write("{0}\t{1}\t{2}\n".format(self.time[i],self.disp[i],self.load[i]))

    @staticmethod
    def open(filename, header=True):
        time = []
        load = []
        disp = []
        with open(filename, 'r') as fh:
            if header:
                for i in range(7):
                    fh.readline()
            line = fh.readline().strip()
            while line != "":
                t, d, l = line.split("\t")
                time.append(float(t))
                load.append(float(l))
                disp.append(float(d))
                line = fh.readline().strip()
        return ASCData(time, load, disp)
