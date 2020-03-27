import numpy as np
import numpy.linalg as la


class ElasticZone:
    def __init__(self, min_lbs, max_lbs):
        self.min_lbs = min_lbs
        self.max_lbs = max_lbs


def linear_regression(x, y):
    """Basic least-squares linear regression"""
    A = np.vstack([x, np.ones(x.shape)]).T
    ret = la.lstsq(A, y)
    m, b = ret[0]
    return m, b, ret[1][0]


def get_yield_line(disp, load):
    m, b, r = linear_regression(disp, load)
    b_offset = m * 0.2
    return m, b - b_offset, r


def suggested_elastic_zone(disp, load):
    """Brute force algorithm for finding a good fitting elastic zone."""
    k_elastic = 0.3
    max_load = np.amax(load)
    n_steps = 100

    # slide the horizontal lines, spaced at deltaHoriz, starting with lower line
    # down at 5% of max load, until the upper line hits 95% of max load.
    start_zone = [max_load * 0.05, max_load * (0.05 + k_elastic)]
    zone = list(start_zone)
    highest_to_go = 0.95 * max_load
    horiz_inc = (highest_to_go - zone[1]) / n_steps
    min_error = None
    iOptimum = 0

    for iStep in range(n_steps):
        zone[0] += horiz_inc
        zone[1] += horiz_inc
        i0 = np.argmin(np.abs(load - zone[0]))
        i1 = np.argmin(np.abs(load - zone[1]))
        m, b, r = linear_regression(disp[i0:i1], load[i0:i1])
        if min_error is None or r < min_error:
            min_error = r
            iOptimum = iStep

    return start_zone[0] + iOptimum * horiz_inc, start_zone[1] + iOptimum * horiz_inc


def line_intersection(xdata, ydata, m, b):
    for i, x in enumerate(xdata):
        if ydata[i] < m * x + b:
            return i
    raise ValueError("Saaaaad")
