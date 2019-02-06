import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from trackerstudies.utils import load_tracking_map_content
from .algorithms import binned_angular_correlation, most_common_scale
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
    _post_process_plot,
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


def plot_tracking_maps_line_vs_reference(
    run_number, reference_run_number, reco, *args, **kwargs
):
    tracking_map = load_tracking_map(run_number, reco)
    tracking_map_content = extract_tracking_map_content(tracking_map)
    reference_map_content = load_tracking_map_content(reference_run_number, reco)

    scale = most_common_scale(tracking_map_content, reference_map_content)
    tracking_map_scaled = tracking_map_content * scale

    max = np.max(reference_map_content)

    tracking_map_normalized = tracking_map_scaled / max
    refrence_map_normalized = reference_map_content / max

    fig, ax = plt.subplots()

    matrix = np.transpose(tracking_map_normalized)
    y = np.reshape(matrix, matrix.size)
    x = np.arange(0, matrix.size)

    matrix_ref = np.transpose(refrence_map_normalized)
    y_ref = np.reshape(matrix_ref, matrix_ref.size)
    x_ref = np.arange(0, matrix_ref.size)

    plt.plot(x, y, alpha=0.75, label=run_number)
    plt.plot(x_ref, y_ref, alpha=0.75, label=reference_run_number)

    plt.legend()
    vals = ax.get_yticks()
    ax.set_yticklabels(["{:,.2%}".format(x) for x in vals])

    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = "{}\n{} (scaled) vs. {} ({})".format(
        extract_tracking_map_title(tracking_map), run_number, reference_run_number, reco
    )

    if kwargs.get("title", None):
        title = "{}\n{}".format(title, kwargs.pop("title"))

    _post_process_plot(xlabel=xlabel, ylabel=ylabel, title=title, *args, **kwargs)


def plot_multiple_tracking_maps_line(run_numbers, reco, *args, **kwargs):
    fig, ax = plt.subplots()

    for run_number in run_numbers:
        tracking_map = load_tracking_map_content(run_number, reco)
        matrix = np.transpose(tracking_map)
        y = np.reshape(matrix, matrix.size)
        x = np.arange(0, matrix.size)
        plt.plot(x, y, label=run_number)

    plt.legend()
    if kwargs.get("save", False) is True:
        kwargs["save"] = "tracking_map_line_{}_{}.pdf".format(run_number, reco)
    _post_process_plot(*args, **kwargs)


def plot_multiple_tracking_maps_line_scaled(run_numbers, reco, *args, **kwargs):
    fig, ax = plt.subplots()

    for run_number in run_numbers:
        tracking_map = load_tracking_map_content(run_number, reco)
        matrix = np.transpose(tracking_map)
        y = np.reshape(matrix, matrix.size)
        x = np.arange(0, matrix.size)
        plt.plot(x, y, label=run_number)

    plt.legend()
    if kwargs.get("save", False) is True:
        kwargs["save"] = "tracking_map_line_{}_{}.pdf".format(run_number, reco)
    _post_process_plot(*args, **kwargs)


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


def plot_reference_subtracted_tracking_map(
    run_number, reference_run_number, reco, *args, **kwargs
):
    tracking_map = load_tracking_map(run_number, reco)
    tracking_map_content = extract_tracking_map_content(tracking_map)
    reference_map_content = load_tracking_map_content(reference_run_number, reco)
    scale = most_common_scale(tracking_map_content, reference_map_content)
    tracking_map_scaled = tracking_map_content * scale
    max = np.max(reference_map_content)

    tracking_map_normalized = tracking_map_scaled / max
    refrence_map_normalized = reference_map_content / max

    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    title = "Subtracted {}\n{} - {} (scaled) ({})".format(
        extract_tracking_map_title(tracking_map), reference_run_number, run_number, reco
    )

    if kwargs.get("title", None):
        title = "{}\n{}".format(title, kwargs.pop("title"))

    plot_matrix(
        refrence_map_normalized - tracking_map_normalized,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        *args,
        **kwargs
    )


def plot_reference_subtracted_tracking_map_3d(
    run_number, reference_run_number, reco, *args, **kwargs
):
    tracking_map = load_tracking_map(run_number, reco)
    xlabel, ylabel = extract_tracking_map_labels(tracking_map)
    matrix = extract_tracking_map_content(tracking_map)

    reference_map = load_tracking_map_content(reference_run_number, reco)
    scale = most_common_scale(matrix, reference_map)
    tracking_map_scaled = matrix * scale
    max = np.max(reference_map)

    tracking_map_normalized = tracking_map_scaled / max
    refrence_map_normalized = reference_map / max

    scale_factor = np.around(scale, decimals=1)

    title = "{}\n{} - {} (scaled * {}) ({})".format(
        extract_tracking_map_title(tracking_map),
        reference_run_number,
        run_number,
        scale_factor,
        reco,
    )

    if kwargs.get("title", None):
        title = "{}\n{}".format(title, kwargs.pop("title"))

    matrix = refrence_map_normalized - tracking_map_normalized

    if not kwargs.get("vmin", None):
        max = np.max(matrix)
        min = np.min(matrix)
        maximum = np.maximum(np.abs(max), np.abs(min))
        kwargs["vmax"] = maximum
        kwargs["vmin"] = -maximum

    plot_3d_matrix(
        matrix,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        use_percent=True,
        *args,
        **kwargs
    )
