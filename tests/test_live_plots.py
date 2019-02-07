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
    plot_reference_subtracted_tracking_map,
    plot_reference_subtracted_tracking_map_3d,
    plot_multiple_tracking_maps_line,
    plot_tracking_maps_line_vs_reference,
    plot_tracking_maps_side_by_side,
    plot_luminosity_lumisection_ratio,
)
from trackerstudies.utils import load_fully_setup_tracker_runs, load_runs


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

    runs = (
        runs.pipe(add_is_bad)
        .pipe(exclude_online)
        .pipe(exclude_rereco)
        .pipe(add_is_commissioning)
        .pipe(add_is_special)
        .pipe(exclude_commissioning)
        .pipe(exclude_special)
    )

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


def test_plot_reference_subtracted_tracking_map():
    run_number = 317512
    reference_run_number = 317435
    reco = "Prompt"

    plot_tracking_map(run_number, reco)
    plot_tracking_map(reference_run_number, reco)

    plot_reference_subtracted_tracking_map(
        run_number, reference_run_number, reco, show=SHOW_PLOTS
    )
    plot_reference_subtracted_tracking_map_3d(
        run_number, reference_run_number, reco, elev=45, azim=35, show=SHOW_PLOTS
    )

    run2 = 319449
    ref2 = 319337

    plot_tracking_map(run2, reco)
    plot_tracking_map(ref2, reco)

    plot_reference_subtracted_tracking_map_3d(
        run2, ref2, reco, elev=45, azim=35, show=SHOW_PLOTS
    )


def test_plot_multiple_tracking_maps_line():
    run_numbers = [317512, 317435, 319337, 319449]
    reco = "Prompt"
    # plot_multiple_tracking_maps_line(run_numbers, reco, show=SHOW_PLOTS)

    run_numbers = [317512, 317435]
    plot_multiple_tracking_maps_line(run_numbers, reco, show=SHOW_PLOTS)

    title = "Bad run"
    plot_tracking_maps_line_vs_reference(
        317512, 317435, reco, title=title, show=SHOW_PLOTS
    )


def test_plot_tracking_maps_side_by_side():
    run_number = 317512
    reference_run_number = 317435
    subtilte = r"452 $ls$, 104.12 $pb^{-1}$"
    plot_tracking_maps_side_by_side(
        run_number,
        reference_run_number,
        "prompt",
        subtitle=subtilte,
        is_bad=False,
        show=True,
    )
    plot_tracking_maps_side_by_side(
        run_number, reference_run_number, "express", is_bad=False
    )


def test_plot_luminosity_lumis_ratio():
    runs = load_runs()
    plot_luminosity_lumisection_ratio(runs)
