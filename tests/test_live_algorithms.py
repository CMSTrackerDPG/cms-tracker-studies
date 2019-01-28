import math

from trackerstudies.algorithms import reference_cost
from trackerstudies.extract import extract_tracking_map_content
from trackerstudies.load import (
    load_tracker_runs,
    load_tkdqmdoctor_runs,
    load_tracking_map,
)
from trackerstudies.merge import merge_runreg_tkdqmdoc


def test_reference_cost():
    run_number = 315322
    ref_run_number = 315705
    expected_cost = 0.130825

    tracker_runs = load_tracker_runs()
    tkdqmdoctor_runs = load_tkdqmdoctor_runs()
    runs = merge_runreg_tkdqmdoc(tracker_runs, tkdqmdoctor_runs)

    runs.set_index(["run_number", "reco"], inplace=True)

    assert runs.loc[(run_number, "prompt"), "reference_run_number"] == ref_run_number

    matrix = extract_tracking_map_content(load_tracking_map(run_number, "prompt"))
    ref_matrix = extract_tracking_map_content(
        load_tracking_map(ref_run_number, "prompt")
    )

    assert math.isclose(reference_cost(matrix, ref_matrix), expected_cost, abs_tol=0.01)
