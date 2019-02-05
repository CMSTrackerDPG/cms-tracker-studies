from tests.conftest import SHOW_PLOTS
from trackerstudies.filters import (
    exclude_online,
    exclude_rereco,
    exclude_cosmics,
    filter_express,
    filter_collisions,
    exclude_commissioning,
    exclude_special,
    filter_run_number_range,
)
from trackerstudies.load import load_tracker_runs, load_tkdqmdoctor_runs
from trackerstudies.merge import merge_runreg_tkdqmdoc
from trackerstudies.pipes import (
    add_is_bad,
    add_is_special,
    add_is_commissioning,
    add_is_heavy_ion,
    add_angular_entropy,
)
from trackerstudies.plots import (
    plot_tracking_map,
    plot_reference_distribution,
    plot_pairs,
    plot_angular_correlation,
    plot_reference_cost,
    plot_angular_entropy,
    plot_referenced_tracking_map_histogram,
    plot_tracking_map_line,
    plot_tracking_map_3d,
)
from trackerstudies.utils import load_fully_setup_tracker_runs


def test_plot_tracking_map():
    run_number = 321755
    reco = "Express"
    plot_tracking_map(run_number, reco, show=SHOW_PLOTS)


def test_plot_tracking_map_3d():
    run_number = 317512
    reference_run_number = 317435
    reco = "Express"
    plot_tracking_map_3d(run_number, reco, show=SHOW_PLOTS)
    plot_tracking_map_3d(reference_run_number, reco, show=SHOW_PLOTS)
    plot_tracking_map_3d(run_number, reco, elev=65, azim=35, show=SHOW_PLOTS)
    plot_tracking_map_3d(reference_run_number, reco, elev=65, azim=35, show=SHOW_PLOTS)


def test_plot_tracking_map_line():
    run_number = 321755
    reco = "Express"
    plot_tracking_map_line(run_number, reco, show=SHOW_PLOTS)
    plot_tracking_map_line(317512, "Prompt", show=SHOW_PLOTS)
    plot_tracking_map_line(317435, "Prompt", show=SHOW_PLOTS)
    plot_tracking_map_line(321755, "Prompt", show=SHOW_PLOTS)
    plot_tracking_map_line(322483, "Prompt", show=SHOW_PLOTS)
    plot_tracking_map_line(322492, "Prompt", show=SHOW_PLOTS)


def test_plot_reference_distribution():
    tracker_runs = load_tracker_runs()

    tkdqmdoctor_runs = load_tkdqmdoctor_runs()
    runs = merge_runreg_tkdqmdoc(tracker_runs, tkdqmdoctor_runs)

    runs = runs.pipe(add_is_bad).pipe(exclude_online).pipe(exclude_rereco)

    plot_reference_distribution(runs, show=SHOW_PLOTS)


def test_plot_pairs():
    tracker_runs = load_tracker_runs()
    plot_pairs(tracker_runs, show=SHOW_PLOTS)


def test_plot_angular_correlation():
    run_number = 321755
    reco = "Express"
    plot_angular_correlation(run_number, reco, show=SHOW_PLOTS)


def test_plot_reference_cost():
    runs = load_fully_setup_tracker_runs()
    runs = runs.pipe(exclude_online).pipe(exclude_rereco).pipe(exclude_cosmics)
    plot_reference_cost(runs, show=SHOW_PLOTS)


def test_plot_angular_entropy():
    runs = (
        load_tracker_runs()
        .pipe(filter_collisions)
        .pipe(filter_express)
        .pipe(add_is_bad)
        .pipe(add_is_special)
        .pipe(add_is_commissioning)
        .pipe(add_is_heavy_ion)
        .pipe(exclude_commissioning)
        .pipe(exclude_special)
        .pipe(filter_run_number_range, 317400, 317500)
        .pipe(add_angular_entropy)
    )

    plot_angular_entropy(runs, show=SHOW_PLOTS, save=SHOW_PLOTS)


def test_plot_referenced_tracking_map_histogram():
    run_number = 317512
    reference_run_number = 317435
    reco = "Prompt"
    plot_referenced_tracking_map_histogram(
        run_number, reference_run_number, reco, show=SHOW_PLOTS
    )
