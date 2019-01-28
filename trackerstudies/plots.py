import seaborn as sns
import matplotlib.pyplot as plt

from .extract import (
    extract_tracking_map_content,
    extract_tracking_map_labels,
    extract_tracking_map_title,
)
from .load import load_tracking_map
from .plotutils import plot_matrix


def plot_tracking_map(run_number, reco, *args, **kwargs):
    tracking_map = load_tracking_map(run_number, reco)
    matrix = extract_tracking_map_content(tracking_map)
    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = extract_tracking_map_title(tracking_map)
    plot_matrix(matrix, xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs)


def plot_reference_distribution(dataframe, *args, **kwargs):
    g = sns.FacetGrid(dataframe, col="reco", row="runtype", hue="is_bad")
    g.map(plt.scatter, "run_number", "reference_run_number", alpha=0.7)

    if kwargs.get("show", False):
        plt.show()


def plot_pairs(dataframe, columns=None, *args, **kwargs):
    raise NotImplementedError


def plot_angular_correleation(matrix, *args, **kwargs):
    raise NotImplementedError
