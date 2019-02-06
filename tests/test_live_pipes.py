import math

from trackerstudies.constants import subdetectors
from trackerstudies.filters import filter_run_number_range
from trackerstudies.load import (
    load_run_registry_json,
    load_tracker_runs,
    load_tkdqmdoctor_runs,
)
from trackerstudies.merge import merge_runreg_tkdqmdoc
from trackerstudies.pipes import (
    unify_columns,
    add_reference_cost,
    add_is_commissioning,
    extract_run_numbers,
    add_all_problems,
)
from trackerstudies.utils import load_merged_tracker_runs


class TestUnify:
    def test_unify_tracker(self):
        runs = load_run_registry_json("tracker")

        assert 9 == len([column for column in runs if column.startswith("rda_cmp")])

        for subdetector in subdetectors:
            assert subdetector not in runs

        runs = unify_columns(runs)

        assert 0 == len([column for column in runs if column.startswith("rda_cmp")])
        assert 36 == len(list(runs))

    def test_unify_global(self):
        runs = load_run_registry_json("global")

        assert 69 == len([column for column in runs if column.startswith("rda_cmp")])

        for subdetector in subdetectors:
            assert subdetector not in runs

        runs = unify_columns(runs)

        for subdetector in subdetectors:
            assert subdetector in runs

        assert 0 == len([column for column in runs if column.startswith("rda_cmp")])
        assert 98 == len(list(runs))


def test_add_reference_cost():
    tracker_runs = load_tracker_runs()
    tkdqmdoc_runs = load_tkdqmdoctor_runs()

    runs = merge_runreg_tkdqmdoc(tracker_runs, tkdqmdoc_runs)

    assert "reference_cost" not in runs
    add_reference_cost(runs)
    assert "reference_cost" in runs

    runs.set_index(["run_number", "reco"], inplace=True)

    assert math.isclose(
        runs.loc[(315322, "prompt"), "reference_cost"], 0.130825, abs_tol=0.01
    )


def test_is_commissioning():
    tracker_runs = load_tracker_runs()

    add_is_commissioning(tracker_runs)

    assert "is_commissioning" in tracker_runs

    tracker_runs.set_index(["run_number", "reco"], inplace=True)

    assert not tracker_runs.loc[(314848, "prompt"), "is_commissioning"]
    assert not tracker_runs.loc[(314848, "express"), "is_commissioning"]
    assert not tracker_runs.loc[(314848, "online"), "is_commissioning"]

    assert not tracker_runs.loc[(321766, "prompt"), "is_commissioning"]
    assert not tracker_runs.loc[(321766, "express"), "is_commissioning"]
    assert not tracker_runs.loc[(321766, "online"), "is_commissioning"]

    assert not tracker_runs.loc[(321773, "prompt"), "is_commissioning"]
    assert not tracker_runs.loc[(321773, "express"), "is_commissioning"]
    assert not tracker_runs.loc[(321773, "online"), "is_commissioning"]

    assert tracker_runs.loc[(314472, "prompt"), "is_commissioning"]
    assert tracker_runs.loc[(314472, "express"), "is_commissioning"]
    assert tracker_runs.loc[(314472, "online"), "is_commissioning"]

    assert tracker_runs.loc[(314541, "express"), "is_commissioning"]
    assert tracker_runs.loc[(314541, "online"), "is_commissioning"]


def test_run_numbers():
    tracker_runs = load_tracker_runs()
    runs = tracker_runs.pipe(filter_run_number_range, 313181, 313183)
    assert set([313181, 313182, 313183]) == set(runs.pipe(extract_run_numbers))


def test_has_problems():
    runs = load_merged_tracker_runs()
    runs = runs.pipe(add_all_problems)

    runs.set_index(["run_number", "reco"], inplace=True)
    assert runs.loc[(319488, "express"), "has_fed_error"], "FED Error in comment"
    assert runs.loc[(324878, "express"), "has_fed_error"], "FED Error in problem names"
    assert not runs.loc[(316653, "prompt"), "has_fed_error"], "No FED Error"

    runs_with_fed_error = [
        319697,
        319882,
        319909,
        320065,
        320920,
        321011,
        321069,
        321149,
        321151,
        321152,
        321153,
        321178,
        321219,
        321221,
        321295,
        321310,
        321311,
        321312,
        321313,
        321397,
        321431,
        321432,
        321777,
        321778,
        321780,
        321973,
        321975,
        322480,
        323109,
        323829,
        323954,
        324231,
        324239,
        324333,
        324410,
        324418,
        324420,
        324878,
        325680,
    ]

    runs.reset_index(inplace=True)

    fed_error_runs = runs[runs.has_fed_error]
    run_numbers = fed_error_runs.pipe(extract_run_numbers)

    for run in runs_with_fed_error:
        assert run in run_numbers

    runs_with_ps_problem = [
        321777,
        321778,
        321780,
        321781,
        322919,
        322922,
        322923,
        322925,
        322928,
        322999,
        323000,
        323001,
        323002,
        323003,
        323097,
        323100,
        323103,
        323104,
        323105,
        323106,
        323107,
        323109,
        323201,
        323202,
        323205,
        323206,
        323207,
    ]
    ps_error_runs = runs[runs.has_ps_problem]
    run_numbers = ps_error_runs.pipe(extract_run_numbers)

    for run in runs_with_ps_problem:
        assert run in run_numbers
