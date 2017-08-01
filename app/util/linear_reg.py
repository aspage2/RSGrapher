
import numpy as np
import numpy.linalg as la

def linear_regression(x,y):
    A = np.vstack([x,np.ones(x.shape)]).T
    return la.lstsq(A,y)