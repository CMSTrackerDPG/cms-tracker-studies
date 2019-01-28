from trackerstudies.load import load_tracker_runs, load_global_runs
from trackerstudies.merge import merge_runreg_runreg


def test_merge_runreg_runreg():
    tracker_runs = load_tracker_runs()
    global_runs = load_global_runs()

    tracker_size = len(tracker_runs)
    global_size = len(global_runs)

    merged = merge_runreg_runreg(tracker_runs, global_runs)
    assert len(merged) == tracker_size + global_size
    assert len(tracker_runs) == tracker_size
    assert len(global_runs) == global_size


def test_merge_runreg_oms():
    pass


def test_merge_runreg_tkdqmdoc():
    pass
