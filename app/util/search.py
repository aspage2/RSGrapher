def nearest_neighbor(x, data):
    """Binary nearest_neighbor searching algorithm"""
    return nearest_neighbor_rec(x, data, 0, len(data) - 1)


def nearest_neighbor_rec(x, data, lo, hi):
    """Return the index of the nearest vale to x in the sorted data on the interval"""
    if lo >= hi:
        return lo
    elif hi - lo == 1:
        if abs(data[hi] - x) < abs(data[lo] - x):
            return hi
        else:
            return lo
    mid = int((hi + lo) / 2)
    if data[mid] == x:
        return mid
    elif data[mid] > x:
        return nearest_neighbor_rec(x, data, lo, mid)
    else:
        return nearest_neighbor_rec(x, data, mid, hi)


def lin_nearest_neighbor(x, data):
    currbest = None
    for i, d in enumerate(data):
        if currbest is None or abs(x-data[currbest]) > abs(x-d):
            currbest = i
    return currbest

def lin_max(data):
    ret = None
    for i, x in enumerate(data):
        if ret is None or data[ret] < x:
            ret = i
    return ret
