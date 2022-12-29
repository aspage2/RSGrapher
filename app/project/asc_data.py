import csv
import numpy as np


class ASCData:
    """Input data from a single stress test (Time, Load, Displacement)"""

    def __init__(self, time=None, load=None, disp=None):
        if time is not None and load is not None and disp is not None:
            self.set_data(time, load, disp)
        else:
            self.time = None
            self.load = None
            self.disp = None

    def set_data(self, time, load, disp):
        self.time = np.array(time)
        self.disp = np.array(disp)
        self.load = np.array(load)

    def __len__(self):
        return len(self.time)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return (
                self.time[key.start : key.stop],
                self.disp[key.start : key.stop],
                self.load[key.start : key.stop],
            )
        return (self.time[key], self.disp[key], self.load[key])

    @staticmethod
    def from_file(filename):
        time = []
        load = []
        disp = []
        with open(filename, "r") as fh:
            rd = csv.reader(fh, dialect="excel-tab")

            # Drop the 7-row header
            for _ in range(7):
                next(rd)

            for t, d, l, *_ in rd:
                time.append(float(t))
                load.append(float(l))
                disp.append(float(d))

        return time, load, disp
