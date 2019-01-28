import pytest

from trackerstudies.exceptions import TrackingMapNotFound
from trackerstudies.load import (
    load_tracker_runs,
    load_global_runs,
    load_tracking_map,
    load_oms_runs,
    load_tkdqmdoctor_runs,
    load_tkdqmdoc_problematic_runs,
    load_all_runreg_runs,
)


class TestTrackingMap:
    def test_load_tracking_map(self):
        tracking_map = load_tracking_map(315252, "Prompt")
        assert "hist" in tracking_map
        assert "TrackEtaPhi_ImpactPoint_GenTk" == tracking_map["hist"]["title"]
        assert 4803330.0 == tracking_map["hist"]["stats"]["entries"]
        assert "content" in tracking_map["hist"]["bins"]

    def test_load_unavailable_tracking_map(self):
        with pytest.raises(TrackingMapNotFound):
            load_tracking_map(215252, "Prompt")


class TestRunRegistry:
    def test_load_tracker_runs(self):
        runs = load_tracker_runs()
        assert "rda_cmp_pixel" not in runs
        assert "rda_cmp_strip" not in runs
        assert "rda_cmp_tracking" not in runs
        assert "rda_cmp_pix" not in runs
        assert "rda_cmp_track" not in runs
        assert "pixel" in runs
        assert "strip" in runs
        assert "tracking" in runs
        assert "csc" not in runs

    def test_load_global_runs(self):
        runs = load_global_runs()
        assert "rda_cmp_pixel" not in runs
        assert "rda_cmp_strip" not in runs
        assert "rda_cmp_tracking" not in runs
        assert "rda_cmp_pix" not in runs
        assert "rda_cmp_track" not in runs
        assert "pixel" in runs
        assert "strip" in runs
        assert "tracking" in runs
        assert "csc" in runs

    def test_load_all_runreg_runs(self):
        tracker_runs = load_tracker_runs()
        global_runs = load_global_runs()
        all_runs = load_all_runreg_runs()
        assert len(all_runs) == len(tracker_runs) + len(
            global_runs
        ), "Increased line count"
        assert len(list(all_runs)) == max(
            len(list(tracker_runs)), len(list(global_runs))
        ), "Maximum column count"


class TestOMS:
    def test_load_oms_runs(self):
        runs = load_oms_runs()
        assert len(runs) >= 6000
        assert len(runs) <= 10000

    def test_load_oms_fills(self):
        pass


class TestTkDQMDoctor:
    def test_load_tkdqmdoctor_runs(self):
        runs = load_tkdqmdoctor_runs()
        assert len(runs) >= 3000
        assert len(runs) <= 4000

    def test_load_tkdqmdoc_problematic_runs(self):
        runs = load_tkdqmdoc_problematic_runs()
        assert len(runs) >= 199
        assert len(runs) <= 300
