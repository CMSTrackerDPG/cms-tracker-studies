import math

import numpy as np
from scipy import stats


def distance(x1, y1, x2, y2):
    # note to self: add phi continuity
    delta_x = x2 - x1
    delta_y = y2 - y1
    return math.sqrt(delta_x ** 2 + delta_y ** 2)


def angular_correlation(matrix):
    # TODO check http://www.astroml.org/user_guide/correlation_functions.html
    # TODO use numpy mathematics

    angular_distances = []
    correlations = []

    for x1 in range(0, np.shape(matrix)[0]):
        for y1 in range(0, np.shape(matrix)[1]):
            for x2 in range(0, np.shape(matrix)[0]):
                for y2 in range(0, np.shape(matrix)[1]):
                    angular_distances.append(distance(x1, y1, x2, y2))
                    correlations.append(math.fabs(matrix[x1][y1] - matrix[x2][y2]))

    return angular_distances, correlations


def binned_angular_correlation(matrix):
    angular_distances, correlations = angular_correlation(matrix)

    bin_means, bin_edges, bin_number = stats.binned_statistic(
        angular_distances, correlations, statistic="mean", bins=50
    )
    bin_width = bin_edges[1] - bin_edges[0]
    bin_centers = bin_edges[1:] - bin_width / 2

    return bin_centers, bin_means


def angular_correlation_entropy(matrix):
    bins, correlations = binned_angular_correlation(matrix)
    return entropy(correlations)


def entropy(data):
    return stats.entropy(data)


def reference_cost(matrix, reference_matrix):
    matrix_normalized = mean_normalize(matrix)
    reference_matrix_normalized = mean_normalize(reference_matrix)
    try:
        return mean_squared_error(matrix_normalized, reference_matrix_normalized)
    except ValueError:
        # Incompatible matrices
        return np.nan


def mean_normalize(data):
    # TODO
    #  RuntimeWarning: invalid value encountered in true_divide
    #  RuntimeWarning: invalid value encountered in greater_equal
    #       keep = (tmp_a >= first_edge)
    #  RuntimeWarning: invalid value encountered in less_equal
    #       keep &= (tmp_a <= last_edge)

    mean = np.mean(data)
    standard_deviation = np.std(data)
    return np.divide(np.subtract(data, mean), standard_deviation)


def mean_squared_error(x, y):
    return ((x - y) ** 2).mean() / 2


def calculate_best_fit_scale(X, Y):
    """
    Requires that at least half of X is similar to Y

    :param X: Matrix X
    :param Y: Refrence Matrix Y
    :return: best factor to scale X to Y
    """
    ratios = np.divide(Y, X)
    return np.median(ratios)
