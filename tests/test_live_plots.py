from tests.conftest import SHOW_PLOTS
from trackerstudies.filters import exclude_online, exclude_rereco
from trackerstudies.load import load_tracker_runs, load_tkdqmdoctor_runs
from trackerstudies.merge import merge_runreg_tkdqmdoc
from trackerstudies.pipes import add_is_bad
from trackerstudies.plots import (
    plot_tracking_map,
    plot_reference_distribution,
    plot_pairs,
    plot_angular_correlation,
)


def test_plot_tracking_map():
    run_number = 321755
    reco = "Express"
    plot_tracking_map(run_number, reco, show=SHOW_PLOTS)


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
