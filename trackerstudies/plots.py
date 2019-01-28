from trackerstudies.extract import (
    extract_tracking_map_content,
    extract_tracking_map_labels,
    extract_tracking_map_title,
)
from trackerstudies.load import load_tracking_map
from trackerstudies.plotutils import plot_matrix


def plot_tracking_map(run_number, reco, *args, **kwargs):
    tracking_map = load_tracking_map(run_number, reco)
    matrix = extract_tracking_map_content(tracking_map)
    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = extract_tracking_map_title(tracking_map)
    plot_matrix(matrix, xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs)


def plot_reference_distribution(dataframe, *args, **kwargs):
    raise NotImplementedError


def plot_pairs(dataframe, columns=None, *args, **kwargs):
    raise NotImplementedError


def plot_angular_correleation(matrix, *args, **kwargs):
    raise NotImplementedError
