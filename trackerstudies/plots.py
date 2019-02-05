import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from trackerstudies.utils import load_tracking_map_content
from .algorithms import binned_angular_correlation
from .extract import (
    extract_tracking_map_content,
    extract_tracking_map_labels,
    extract_tracking_map_title,
)
from .load import load_tracking_map
from .plotutils import (
    plot_matrix,
    plot_line,
    save_with_default_name,
    plot_histogram,
    plot_3d_matrix,
)


def plot_tracking_map(run_number, reco, *args, **kwargs):
    tracking_map = load_tracking_map(run_number, reco)
    matrix = extract_tracking_map_content(tracking_map)
    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = "{}\n{} ({})".format(
        extract_tracking_map_title(tracking_map), run_number, reco
    )

    if kwargs.get("save", False) is True:
        kwargs["save"] = "tracking_map_{}_{}.pdf".format(run_number, reco)

    plot_matrix(matrix, xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs)


def plot_tracking_map_3d(run_number, reco, *args, **kwargs):
    tracking_map = load_tracking_map(run_number, reco)
    matrix = extract_tracking_map_content(tracking_map)
    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = "{}\n{} ({})".format(
        extract_tracking_map_title(tracking_map), run_number, reco
    )

    if kwargs.get("save", False) is True:
        kwargs["save"] = "tracking_map_3d_{}_{}.pdf".format(run_number, reco)

    plot_3d_matrix(matrix, xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs)


def plot_tracking_map_line(run_number, reco, *args, **kwargs):
    tracking_map = load_tracking_map(run_number, reco)
    matrix = extract_tracking_map_content(tracking_map)
    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = "{}\n{} ({})".format(
        extract_tracking_map_title(tracking_map), run_number, reco
    )

    matrix = np.transpose(matrix)
    y = np.reshape(matrix, matrix.size)
    x = np.arange(0, matrix.size)

    if kwargs.get("save", False) is True:
        kwargs["save"] = "tracking_map_line_{}_{}.pdf".format(run_number, reco)

    plot_line(x, y, xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs)


def plot_reference_distribution(dataframe, *args, **kwargs):
    g = sns.FacetGrid(dataframe, col="reco", row="runtype", hue="is_bad")
    g.map(plt.scatter, "run_number", "reference_run_number", alpha=0.7)

    save_with_default_name(kwargs.get("save", False), "reference_distribution.pdf")

    if kwargs.get("show", False):
        plt.show()


def plot_pairs(dataframe, columns=None, *args, **kwargs):
    columns = (
        columns
        if columns
        else ["run_number", "lhc_fill", "lumisections", "run_lumi", "run_live_lumi"]
    )

    sns.pairplot(dataframe[columns])

    save_with_default_name(kwargs.get("save", False), "pair_plot.pdf")

    if kwargs.get("show", False):
        plt.show()


def plot_angular_correlation(run_number, reco, *args, **kwargs):
    tracking_map = load_tracking_map(run_number, reco)
    matrix = extract_tracking_map_content(tracking_map)
    bins, correlation = binned_angular_correlation(matrix)

    xlabel = "Binned Two Point Distance"
    ylabel = "Average Delta Occupancy"
    title = "Angular correlation {} ({})".format(run_number, reco)

    if kwargs.get("save", False) is True:
        kwargs["save"] = "angular_correlation_{}_{}.pdf".format(run_number, reco)

    plot_line(
        bins, correlation, xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs
    )


def plot_reference_cost(dataframe, *args, **kwargs):
    g = sns.FacetGrid(dataframe, col="reco", row="runtype", hue="is_bad")
    g = g.map(plt.scatter, "run_number", "reference_cost", alpha=0.7)

    save_with_default_name(kwargs.get("save", False), "reference_cost.pdf")

    if kwargs.get("show", False):
        plt.show()


def plot_angular_entropy(dataframe, *args, **kwargs):
    g = sns.FacetGrid(dataframe, col="reco", row="runtype", hue="is_bad")
    g.map(plt.scatter, "run_number", "angular_entropy", alpha=0.7)

    save_with_default_name(kwargs.get("save", False), "angular_entropy.pdf")

    if kwargs.get("show", False):
        plt.show()


def plot_referenced_tracking_map_histogram(
    run_number, reference_run_number, reco, *args, **kwargs
):
    tk_map = load_tracking_map_content(run_number, reco)
    reference_map = load_tracking_map_content(reference_run_number, reco)
    ratios = np.divide(tk_map, reference_map)
    title = "{} vs {} ({})".format(run_number, reference_run_number, reco)
    if kwargs.get("title", None):
        title = "{}\n{}".format(title, kwargs.pop("title"))

    plot_histogram(ratios, title=title, *args, **kwargs)
