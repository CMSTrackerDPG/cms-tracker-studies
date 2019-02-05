import math

import numpy

from trackerstudies.algorithms import (
    reference_cost,
    scaled_reference_cost,
    most_common_scale,
)


def test_reference_cost():
    A = numpy.array([[1, 2], [3, 4]])
    B = numpy.array([[1, 2], [3, 4]])

    assert 0 == reference_cost(A, B)

    A = numpy.array([[1, 1], [3, 4]])
    B = numpy.array([[1, 2], [3, 4]])

    assert 0 < reference_cost(A, B)
    assert 0 != reference_cost(A, B)
    assert numpy.inf != reference_cost(A, B)

    A = numpy.array([[0, 0], [0, 0]])
    B = numpy.array([[1, 2], [3, 4]])

    assert numpy.inf == reference_cost(A, B)


def test_scaled_reference_cost():
    A = numpy.array([[1, 2], [3, 4]])
    B = numpy.array([[1, 2], [3, 4]])

    assert 0 == scaled_reference_cost(A, B)

    A = numpy.array([[1, 1], [3, 4]])
    B = numpy.array([[1, 2], [3, 4]])

    assert 0 < scaled_reference_cost(A, B)
    assert 0 != scaled_reference_cost(A, B)
    assert not numpy.isnan(scaled_reference_cost(A, B))

    A = numpy.array([[0, 0], [0, 0]])
    B = numpy.array([[1, 2], [3, 4]])

    assert not numpy.isnan(scaled_reference_cost(A, B))


class TestMostCommonScale:
    def test_trivial_case(self):
        A = numpy.array([[1, 2], [3, 4]])
        B = numpy.array([[1, 2], [3, 4]])
        assert 1 == most_common_scale(A, B)

    def test_scale_two(self):
        A = numpy.array([[1, 2], [3, 4]])
        B = numpy.array([[2, 4], [6, 8]])
        assert 2 == most_common_scale(A, B)

    def test_scale_two_float(self):
        A = numpy.array([[1, 2], [3, 4]])
        B = numpy.array([[2.01, 4], [6, 8.01]])
        assert 2 == most_common_scale(A, B)

    def test_scale_single_error(self):
        A = numpy.array([[1, 2], [3, 4]])
        B = numpy.array([[2, 4], [6, 9]])
        assert 2 == most_common_scale(A, B)

    def test_scale_two_error(self):
        A = numpy.array([[1, 2], [3, 4]])
        B = numpy.array([[2, 5], [6, 9]])
        assert 2 == most_common_scale(A, B)

    def test_scale_three_error(self):
        A = numpy.array([[1, 2], [3, 4], [5, 6]])
        B = numpy.array([[2, 5], [6, 9], [10, 11]])
        assert 2 == most_common_scale(A, B)

    def test_all_differ_slightly(self):
        A = numpy.array([[1, 2], [3, 4], [5, 6]])
        B = numpy.array([[3.01, 6.01], [9.01, 12.01], [15.01, 18.01]])
        assert math.isclose(3.002, most_common_scale(A, B))

    def test_all_but_two_are_wrong(self):
        A = numpy.array([[1, 2], [3, 4], [5, 6]])
        B = numpy.array([[3.01, 8.01], [2.01, 19.01], [11.01, 18.01]])
        assert math.isclose(3, most_common_scale(A, B), abs_tol=0.01)

    def test_one_is_zero(self):
        A = numpy.array([[1, 0], [3, 4]])
        B = numpy.array([[-1, -2], [-3, -4]])
        assert -1 == most_common_scale(A, B)

    def test_most_are_zero(self):
        A = numpy.array([[0, 0], [6, 0]])
        B = numpy.array([[-1, -2], [-3, -4]])
        assert -0.5 == most_common_scale(A, B)

    def test_all_are_zero(self):
        A = numpy.array([[0, 0], [0, 0]])
        B = numpy.array([[-1, -2], [-3, -4]])
        assert numpy.isnan(most_common_scale(A, B))

    def test_reference_is_zero(self):
        A = numpy.array([[1, 2], [3, 4]])
        B = numpy.array([[-2, 0], [-6, -8]])
        assert -2 == most_common_scale(A, B)

    def test_reference_two_are_zero(self):
        A = numpy.array([[1, 2], [3, 4], [5, 6]])
        B = numpy.array([[2, 0], [6, -0], [10, 12]])
        assert 2 == most_common_scale(A, B)

    def test_reference_all_zero(self):
        A = numpy.array([[1, 2], [3, 4], [5, 6]])
        B = numpy.array([[0, 0], [0, -0], [0, 0]])
        assert 0 == most_common_scale(A, B)
