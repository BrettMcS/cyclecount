# test_rainflow.py

import sys
sys.path.insert(0, '..\\rainflow')

import numpy as np

import rainflow


def test_ranges_means():

    data = np.array([-9, 5, -3, 9, 3, 7, -5, -3, -9], dtype=np.int16)
    range_ans = [8, 4, 2, 18]
    mean_ans = [1.0, 5.0, -4.0, 0.0]

    ranges, means = rainflow._ranges_means(data)

    assert ranges == range_ans
    assert means == mean_ans


def test_get_ranges_and_means():

    data = np.array([-5.0, -5.0, -3.0, -9.0, -9.0, 5.0, -3.0, 9.0, 3.0, 7.0])
    range_ans = np.array([8.0, 4.0, 2.0, 18.0])
    mean_ans = np.array([1.0, 5.0, -4.0, 0.0])

    ranges, means = rainflow.get_ranges_and_means(data)

    assert np.alltrue(ranges == range_ans)
    assert np.alltrue(means == mean_ans)
