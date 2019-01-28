from trackerstudies.constants import subdetectors
from trackerstudies.load import load_run_registry_json
from trackerstudies.pipes import unify_columns


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
