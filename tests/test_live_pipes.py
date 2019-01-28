import math

from trackerstudies.constants import subdetectors
from trackerstudies.load import (
    load_run_registry_json,
    load_tracker_runs,
    load_tkdqmdoctor_runs,
)
from trackerstudies.merge import merge_runreg_tkdqmdoc
from trackerstudies.pipes import unify_columns, add_reference_cost, add_is_commissioning


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
