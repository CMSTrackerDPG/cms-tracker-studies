import pytest

from trackerstudies.exceptions import TrackingMapNotFound
from trackerstudies.load import (
    load_tracker_runs,
    load_global_runs,
    load_tracking_map,
    load_oms_runs,
    load_tkdqmdoctor_runs,
    load_tkdqmdoctor_problem_runs,
    load_all_runreg_runs,
    read_histogram_folder,
    load_all_histogram_folders,
    load_online_tracker_runs,
    load_oms_fills,
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

    def test_load_online_tracker_runs(self):
        runs = load_online_tracker_runs()

        to_exclude = [
            "dt",
            "l1t",
            "tau_cause",
            "lumi_comment",
            "tau_comment",
            "hlt_cause",
            "muon",
            "cms",
            "hcal_comment",
            "rpc_cause",
            "es_cause",
            "l1tcalo",
            "l1t_comment",
            "dt_cause",
            "csc_comment",
            "lowlumi_cause",
            "ecal_comment",
            "lumi_cause",
            "btag_comment",
            "es",
            "ctpps_comment",
            "jetmet_cause",
            "egamma_cause",
            "hlt_comment",
            "egamma",
            "rpc_comment",
            "ctpps",
            "egamma_comment",
            "l1tcalo_comment",
            "dt_comment",
            "ctpps_cause",
            "l1tmu",
            "tau",
            "cms_comment",
            "run_short",
            "hlt",
            "hcal_cause",
            "hcal",
            "l1t_cause",
            "l1tmu_cause",
            "l1tcalo_cause",
            "cms_cause",
            "run_test",
            "castor_comment",
            "btag",
            "jetmet_comment",
            "muon_cause",
            "rpc",
            "ecal_cause",
            "csc",
            "csc_cause",
            "es_comment",
            "castor_cause",
            "castor",
            "muon_comment",
            "lowlumi",
            "ecal",
            "l1tmu_comment",
            "btag_cause",
            "jetmet",
            "lumi",
            "lowlumi_comment",
        ]

        for column in to_exclude:
            assert column not in runs

        assert "pixel" in runs
        assert "strip" in runs
        assert "tracking" in runs

        assert list(runs.reco.unique()) == ["online"]
        print()
        print(runs[["run_number", "pixel", "strip", "tracking"]])
        print(sorted(list(runs.tracking.unique())))
        print(sorted(list(runs.rda_state.unique())))
        print(len(runs[runs.rda_state == "OPEN"]))
        print(len(runs[runs.rda_state == "SIGNOFF"]))

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
        fills = load_oms_fills()
        assert fills.loc[0, "fill_number"] == 6477
        assert fills.loc[len(fills) - 1, "fill_number"] == 7492
        assert len(fills) >= 1000


class TestTkDQMDoctor:
    def test_load_tkdqmdoctor_runs(self):
        runs = load_tkdqmdoctor_runs()
        assert len(runs) >= 3000
        assert len(runs) <= 4000

    def test_load_tkdqmdoc_problematic_runs(self):
        runs = load_tkdqmdoctor_problem_runs()
        assert len(runs) >= 199
        assert len(runs) <= 300


def test_read_histogram_folder():
    df = read_histogram_folder("NumberOfRecHitsPerTrack_GenTk", attribute_prefix="hits")

    assert len(df) >= 975
    assert len(df.columns) == 4


def test_read_all_histogram_folders():
    df = load_all_histogram_folders()

    assert len(df) >= 975
    assert len(df.columns) >= 77 * 4
