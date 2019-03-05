import pandas

from trackerstudies.utils import (
    load_fully_setup_tracker_runs,
    load_fully_setup_global_runs,
    load_all_workspaces_full_setup,
    load_runs,
)


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
    assert {"tracker"} == set(runs.workspace.unique())


def test_load_fully_setup_global_runs():
    runs = load_fully_setup_global_runs()

    assert "runtype" in runs
    assert "is_bad" in runs
    assert "is_heavy_ion" in runs
    assert "is_commissioning" in runs
    assert "is_special" in runs
    assert "reference_cost" in runs
    assert "is_heavy_ion" in runs
    assert {"prompt", "rereco"} == set(runs.reco.unique())
    assert {"cosmics", "collisions"} == set(runs.runtype.unique())
    assert {"global"} == set(runs.workspace.unique())


def test_load_all_workspaces_full_setup():
    runs = load_all_workspaces_full_setup()

    assert "runtype" in runs
    assert "is_bad" in runs
    assert "is_heavy_ion" in runs
    assert "is_commissioning" in runs
    assert "is_special" in runs
    assert "reference_cost" in runs
    assert "is_heavy_ion" in runs
    assert {"express", "prompt", "rereco"} == set(runs.reco.unique())
    assert {"cosmics", "collisions"} == set(runs.runtype.unique())
    assert {"tracker", "global"} == set(runs.workspace.unique())


def test_load_runs():
    runs = load_runs()
    assert len(runs) > 5000
    assert len(runs.columns) >= 436

    runs.reco = pandas.Categorical(runs.reco, ["online", "express", "prompt", "rereco"])

    runs = runs.sort_values(["run_number", "reco"]).reset_index()

    bad_online = list(
        runs[(runs.reco == "online") & (runs.tracking == "BAD")].run_number.unique()
    )

    runs = runs[runs.run_number.isin(bad_online)]
    print()
    print(bad_online)
    print()
    print(runs[["run_number", "reco", "runtype", "pixel", "strip", "tracking"]])
