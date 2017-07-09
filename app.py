import csv
# import xlsxwriter
import numpy as np
from scipy import stats
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # Do not do this prior to calling use()
import math
from numpy import genfromtxt
import copy


class ElasticZone():
    def __init__(self, min_lbs, max_lbs):
        self.min_lbs = min_lbs
        self.max_lbs = max_lbs


class YieldPointStruct():
    pass


# -------------------------------------------------------------------------------
#                                                  G E T   Y I E L D   P O I N T
def getYieldPoint(disp_in, load_lbs, interval):
    YieldPoint = YieldPointStruct()

    # Trim off everything but what is in the zone
    N = len(disp_in)
    indxArray = np.arange(0, N, 1)
    indxArray = indxArray[np.where((load_lbs[:] > interval.min_lbs) & (load_lbs[:] < interval.max_lbs))]
    EzoneDisp = disp_in[indxArray]
    EzoneLoad = load_lbs[indxArray]
    #     // Linear estimate for the load versus displacement curve, over the section
    #     // that the two horizontal lines of "ElasticZone"
    #     //y=mx+b, or load=m*disp + b
    YieldPoint.m, YieldPoint.b, r_value, p_value, YieldPoint.std_err = stats.linregress(EzoneDisp, EzoneLoad)

    #     // Standard Method
    #     // Ductile metals do not have a well defined yield point. The yield strength is
    #     // typically defined by the "0.2% offset strain". The yield strength at 0.2%
    #     // offset is determined by finding the intersection of the stress-strain curve
    #     // with a line parallel to the initial slope of the curve and which
    #     // intercepts the abscissa at 0.2%.
    #     //
    #     //

    pctOffst = 0.2  # Percent Strain, where Strain is defined to be displacement/PullLength
    #     // PullLength is the length of the sample between the points where the machine
    #     // is grabbing onto.

    #     // keeping in the raw-data units, so figure inches of displacement for the pctOffst Strain.
    PullLength_in_ = 50.3
    HorizOffset_in = (pctOffst / 100) * PullLength_in_

    YieldPoint.Offset_b = YieldPoint.b - YieldPoint.m * HorizOffset_in
    #     // start looking for point of intersection somewhere beyond disp_in(indxArray($))

    i = indxArray[-1]
    while ((load_lbs[i] > YieldPoint.m * disp_in[i] + YieldPoint.Offset_b)
               &
               (i < (N - 1))):
        i = i + 1

    YieldPoint.disp_in = disp_in[i]
    YieldPoint.load_lbs = load_lbs[i]
    return YieldPoint


# -------------------------------------------------------------------------------


def getAutoElasticZone(disp_in, load_lbs):
    kElastic = 0.3  # // fraction of the max load.  this is dist between horiz lines.
    MaxLoad = np.amax(load_lbs)
    Nsteps = 100

    #     // slide the horizontal lines, spaced at deltaHoriz, starting with lower line
    #     // down at 5% of max load, until the upper line hits 95% of max load.
    StartElasticZone = ElasticZone(MaxLoad * 0.05, MaxLoad * (0.05 + kElastic))
    SlidingElasticZone = copy.copy(StartElasticZone)
    HighestToGo = 0.95 * MaxLoad
    HorizInc = (HighestToGo - StartElasticZone.max_lbs) / Nsteps
    MinError = np.inf
    iOptimum = 0

    for iStep in range(0, Nsteps):
        SlidingElasticZone.min_lbs = StartElasticZone.min_lbs + iStep * HorizInc
        SlidingElasticZone.max_lbs = StartElasticZone.max_lbs + iStep * HorizInc

        err = getYieldPoint(disp_in, load_lbs, SlidingElasticZone).std_err
        if err < MinError:
            MinError = err
            iOptimum = iStep

    return ElasticZone(StartElasticZone.min_lbs + iOptimum * HorizInc,
                       StartElasticZone.max_lbs + iOptimum * HorizInc, )
