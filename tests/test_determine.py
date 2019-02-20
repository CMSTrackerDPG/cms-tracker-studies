import numpy

from trackerstudies.determine import (
    determine_tracker_is_bad,
    determine_runtype,
    determine_is_certification_status_summary,
)


def test_determine_is_bad():
    assert not determine_tracker_is_bad("good", "good", "good", "cosmics")
    assert not determine_tracker_is_bad("bad", "good", "good", "cosmics")
    assert determine_tracker_is_bad("good", "bad", "good", "cosmics")
    assert determine_tracker_is_bad("good", "good", "bad", "cosmics")
    assert determine_tracker_is_bad("bad", "bad", "bad", "cosmics")

    assert not determine_tracker_is_bad("good", "good", "good", "collisions")
    assert determine_tracker_is_bad("bad", "good", "good", "collisions")
    assert determine_tracker_is_bad("bad", "good", "good", "collisions")
    assert determine_tracker_is_bad("good", "bad", "good", "collisions")
    assert determine_tracker_is_bad("good", "good", "bad", "collisions")
    assert determine_tracker_is_bad("bad", "bad", "bad", "collisions")


def test_determine_runtype():
    assert numpy.isnan(determine_runtype("Commissioning18"))
    assert "cosmics" == determine_runtype("Cosmics18")
    assert "collisions" == determine_runtype("Collisions18")
    assert numpy.isnan(determine_runtype("SomethinngCompletelyWrong"))
    assert "collisions" == determine_runtype("Collisions18SpecialRun")


def test_determine_is_certification_status_summary():
    assert "Good" == determine_is_certification_status_summary("GOOD", "GOOD", "GOOD")
    assert "Bad" == determine_is_certification_status_summary("BAD", "BAD", "BAD")
    assert "Pixel Excluded" == determine_is_certification_status_summary(
        "EXCLUDED", "GOOD", "BAD"
    )
    assert "Strip Bad" == determine_is_certification_status_summary(
        "GOOD", "BAD", "GOOD"
    )
