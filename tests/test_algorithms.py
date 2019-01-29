import numpy

from trackerstudies.algorithms import calculate_best_fit_scale


class TestBestFitScale:
    def test_trivial_case(self):
        X = numpy.array([[1, 2], [3, 4], [5, 6]])
        Y = numpy.array([[1, 2], [3, 4], [5, 6]])

        assert 1 == calculate_best_fit_scale(X, Y)

    def test_factor_two(self):
        X = numpy.array([[1, 2], [3, 4], [5, 6]])
        Y = numpy.array([[2, 4], [6, 8], [10, 12]])

        assert 2 == calculate_best_fit_scale(X, Y)

    def test_factor_half(self):
        X = numpy.array([[2, 4], [6, 8], [10, 12]])
        Y = numpy.array([[1, 2], [3, 4], [5, 6]])

        assert 0.5 == calculate_best_fit_scale(X, Y)

    def test_factor_two_single_error(self):
        X = numpy.array([[1, 2], [3, 4], [5, 6]])
        Y = numpy.array([[2, 4], [7, 8], [10, 12]])

        assert 2 == calculate_best_fit_scale(X, Y)

    def test_factor_two_multiple_error(self):
        X = numpy.array([[1, 2], [3, 4], [5, 6]])
        Y = numpy.array([[2, 3], [7, 8], [11, 12]])

        assert 2 == calculate_best_fit_scale(X, Y)

    def test_factor_two_multiple_error(self):
        X = numpy.array([[1, 2], [3, 4], [5, 6]])
        Y = numpy.array([[2, 4], [6, 9], [10, 13]])

        assert 2 == calculate_best_fit_scale(X, Y)
