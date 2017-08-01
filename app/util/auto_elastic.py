from app.util.linear_reg import linear_regression
import numpy as np


class ElasticZone():
    def __init__(self, min_lbs, max_lbs):
        self.min_lbs = min_lbs
        self.max_lbs = max_lbs


def get_yield_line(sample):
    time, disp, load = sample.elastic_interval_data()
    line, residual = linear_regression(disp, load)[:2]
    m, b = line
    r = residual[0]
    b_offset = m * 0.2 / 100.0 * sample.length
    return m, b - b_offset, r


def getAutoElasticZone(sample):
    kElastic = 0.3  # // fraction of the max load.  this is dist between horiz lines.
    time, disp, load_lbs = sample.test_interval_data()
    MaxLoad = np.amax(load_lbs)
    Nsteps = 100

    #     // slide the horizontal lines, spaced at deltaHoriz, starting with lower line
    #     // down at 5% of max load, until the upper line hits 95% of max load.
    start_elastic_zone = ElasticZone(MaxLoad * 0.05, MaxLoad * (0.05 + kElastic))
    highest_to_go = 0.95 * MaxLoad
    horiz_inc = (highest_to_go - start_elastic_zone.max_lbs) / Nsteps
    min_error = None
    iOptimum = 0
    m_opt = 0
    b_opt = 0

    for iStep in range(Nsteps):
        sample.set_elastic_interval(start_elastic_zone.min_lbs + iStep * horiz_inc,
                                    start_elastic_zone.max_lbs + iStep * horiz_inc)
        m, b, r = get_yield_line(sample)
        if min_error is None or r < min_error:
            min_error = r
            iOptimum = iStep
            m_opt = m
            b_opt = b

    sample.set_elastic_interval(start_elastic_zone.min_lbs + iOptimum * horiz_inc,
                                start_elastic_zone.max_lbs + iOptimum * horiz_inc)

    return m_opt, b_opt
