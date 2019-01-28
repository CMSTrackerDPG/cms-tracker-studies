from trackerstudies.utils import load_fully_setup_tracker_runs


def test_load_fully_setup_tracker_runs():
    runs = load_fully_setup_tracker_runs()

    assert "runtype" in runs
    assert "is_bad" in runs
    assert "is_heavy_ion" in runs
    assert "is_commissioning" in runs
    assert "is_special" in runs
    assert "reference_cost" in runs
    assert "is_heavy_ion" in runs
    assert {"express", "prompt", "rereco"} == set(runs.reco.unique())
    assert {"cosmics", "collisions"} == set(runs.runtype.unique())
