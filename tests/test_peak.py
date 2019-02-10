# test_peak.py

import sys
sys.path.insert(0, '..\\rainflow')

import numpy as np

from rainflow import _get_peaks


def test_get_peaks():

    data1 = np.array([4, 0, -1, -3, 2, 0, 7, 9])
    ans1 = np.array([9, -3, 2, 0, 9])

    data2 = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    ans2 = np.array([5.0, 0.0, 5.0])

    data3 = np.array([1, 1, 1, 1])

    peaks1 = _get_peaks(data1)
    peaks2 = _get_peaks(data2)
    peaks3 = _get_peaks(data3)

    assert np.alltrue(peaks1 == ans1)
    assert np.alltrue(peaks2 == ans2)
    assert len(peaks3) == 0
