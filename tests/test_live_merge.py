from trackerstudies.load import (
    load_tracker_runs,
    load_global_runs,
    load_oms_runs,
    load_tkdqmdoctor_runs,
)
from trackerstudies.merge import (
    merge_runreg_runreg,
    merge_runreg_oms,
    merge_runreg_tkdqmdoc,
)


def test_merge_runreg_runreg():
    tracker_runs = load_tracker_runs()
    global_runs = load_global_runs()

    tracker_size = len(tracker_runs)
    global_size = len(global_runs)

    tracker_column_count = len(list(tracker_runs))
    global_column_count = len(list(global_runs))

    assert global_column_count > tracker_column_count

    merged = merge_runreg_runreg(tracker_runs, global_runs)

    assert len(merged) == tracker_size + global_size, "Line Count increased"
    assert len(list(merged)) == global_column_count, "Column Count is maximum"
    assert len(tracker_runs) == tracker_size, "Nothing changed in tracker runs"
    assert len(global_runs) == global_size, "Nothing changed in global runs"
    assert global_column_count > tracker_column_count


def test_merge_runreg_oms():
    tracker_runs = load_tracker_runs()
    oms = load_oms_runs()

    tracker_size = len(tracker_runs)
    tracker_column_count = len(list(tracker_runs))
    oms_column_count = len(list(oms))

    assert 36 == tracker_column_count
    assert 35 == oms_column_count

    merged = merge_runreg_oms(tracker_runs, oms)

    merged_column_count = len(list(merged))

    assert len(tracker_runs) == tracker_size, "No Change in Line count"
    assert (
        tracker_column_count + oms_column_count - 1 == merged_column_count
    ), "Increased Column count"


def test_merge_runreg_oms():
    tracker_runs = load_tracker_runs()
    tkdqm = load_tkdqmdoctor_runs()

    tracker_size = len(tracker_runs)
    tracker_column_count = len(list(tracker_runs))

    assert 36 == tracker_column_count

    merged = merge_runreg_tkdqmdoc(tracker_runs, tkdqm)
    merged_column_count = len(list(merged))

    assert len(tracker_runs) == tracker_size, "No Change in Line count"
    assert tracker_column_count + 1 == merged_column_count, "Increased Column count"
