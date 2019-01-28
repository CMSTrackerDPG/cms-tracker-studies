import os

import numpy

from trackerstudies.plotutils import plot_matrix, plot_line


def test_plot_matrix():
    matrix = numpy.array([[1, 2, 3], [4, 5, 6]])
    file_name = "colored-matrix.pdf"
    assert not os.path.isfile(file_name)
    plot_matrix(
        matrix,
        xlabel="A x axis",
        ylabel="Some y axis",
        title="A colored Matrix",
        show=True,
        save=file_name,
    )
    assert os.path.isfile(file_name)
    os.remove(file_name)
    assert not os.path.isfile(file_name)


def test_plot_line():
    x = numpy.array([1, 2, 4, 5])
    y = numpy.array([4, 2, 8, 1])
    file_name = "line-plot.pdf"
    assert not os.path.isfile(file_name)
    plot_line(
        x,
        y,
        xlabel="A x axis",
        ylabel="Some y axis",
        title="A Line",
        show=True,
        save=file_name,
    )
    assert os.path.isfile(file_name)
    os.remove(file_name)
    assert not os.path.isfile(file_name)
