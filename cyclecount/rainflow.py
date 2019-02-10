# rainflow.py
"""
Rainflow cycle counting function based on Downing's Method 1 of the 
paper "Simple rainflow counting algorithms" by S.D.Downing and D.F.Socie
International Journal of Fatigue, January 1982.

This method is for limited histories where the data has been obtained 
and stored. Method 2 from the same paper (not implemented here) is 
designed for open-ended histories, typically in a monitoring situation.

Method 1 requires that the signal be first re-arranged so that signal 
starts and finishes with the largest (magnitude) peak or trough (we just
say 'peak' to include both from now on). This is done in the function
_get_peaks
"""
import numpy as np
from numba import jit


def get_integral_data(raw_data, scale):
    """
    Returns nearest_int_to(raw_data * scale) as int32s.

    :Parameters:
        raw_data: 1D ndarray
        scale: float. Multiply raw_data by this before taking int()

    :Returns:
        ndarray. (raw_data * scale) and rounded to nearest int32
    """
    return np.array(np.rint(raw_data * scale), dtype=np.int32)


def get_ranges_and_means(data):
    """
    Return ranges, means of a 1D array using Rainflow cycle counting

    :Parameters:
        raw_data: 1-D ndarray. The data to be analysed. Int or float.

    :Returns:
        ranges, means: 1D ndarrays. The cycle ranges and mean values

    :References:
        Rainflow cycle counting method based on Downing's Method 1 of 
        the paper "Simple rainflow counting algorithms" by S.D.Downing
        and D.F.Socie, International Journal of Fatigue, January 1982.
    """
    peaks = _get_peaks(data)

    if len(peaks) == 0:
        return [], []

    ranges, means = _ranges_means(peaks)

    return np.array(ranges), np.array(means)


def _get_peaks(data):
    """
    Return peaks & troughs of data, starting & finishing at the maximum
    """
    # eliminate repeated data points:
    data = data[data != np.roll(data, 1)]

    if len(data) == 0:
        return []

    # split and rejoin at largest abs value
    max_idx = np.argmax(np.abs(data))
    data = np.concatenate((data[max_idx:], data[:max_idx]))

    # find peaks and troughs
    prv = np.roll(data, -1)
    nxt = np.roll(data, 1)

    isPeak = ((data > prv) & (data > nxt)) | ((data < prv) & (data < nxt))

    # Close off the signal with the max (ie first) value, as required.
    return np.concatenate((data[isPeak], data[:1]))  


@jit(nopython=True)  # gives ~20x speed improvement
def _ranges_means(peaks):
    """
    Return ranges, means of cycles counted using Downing's method 1.
    """
    values = []  # of the current peaks being processed
    ranges = []
    means = []

    for peak in peaks:
        values.append(peak)
        while len(values) > 2:
            X = abs(values[-1] - values[-2])
            Y = abs(values[-2] - values[-3])
            if X < Y:
                break
            ranges.append(Y)
            means.append(0.5*(values[-2] + values[-3]))
            values[-3] = values[-1]
            values.pop()
            values.pop()

    return ranges, means
