from trackerstudies.determine import determine_tracker_is_bad


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
