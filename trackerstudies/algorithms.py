import numpy


def reference_cost(matrix, reference_matrix):
    matrix_normalized = mean_normalize(matrix)
    reference_matrix_normalized = mean_normalize(reference_matrix)
    return mean_squared_error(matrix_normalized, reference_matrix_normalized)


def mean_normalize(data):
    mean = numpy.mean(data)
    standard_deviation = numpy.std(data)
    return numpy.divide(numpy.subtract(data, mean), standard_deviation)


def mean_squared_error(x, y):
    return ((x - y) ** 2).mean() / 2
