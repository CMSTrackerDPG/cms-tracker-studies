import numpy

from trackerstudies.determine import determine_tracker_is_bad, determine_run_type


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
    assert numpy.isnan(determine_run_type("/Express/Commissioning2018/DQM", "Commissioning18"))
    assert numpy.isnan(determine_run_type("/Global/Online/ALL", "Commissioning18"))

    assert "cosmics" == determine_run_type("/Express/Cosmics2018/DQM", "Cosmics18")
    assert "cosmics" == determine_run_type("/Global/Online/ALL", "Cosmics18")
    assert "cosmics" == determine_run_type("/PromptReco/Cosmics18/DQM", "Cosmics18")

    assert "collisions" == determine_run_type("/Express/Collisions2018/DQM", "Collisions18")
    assert "collisions" == determine_run_type("/Global/Online/ALL", "Collisions18")
    assert "collisions" == determine_run_type("/PromptReco/Collisions2018Commiss/DQM", "Collisions18")
