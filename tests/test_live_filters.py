from trackerstudies.filters import (
    exclude_collisions,
    exclude_lumisections_gte,
    exclude_prompt,
    exclude_express,
    exclude_rereco,
    exclude_online,
    filter_online,
    filter_lumisections_gte,
    filter_express,
    filter_prompt,
    filter_collisions,
    filter_rereco,
    filter_cosmics,
    exclude_cosmics,
)
from trackerstudies.load import load_tracker_runs


class TestFilter:
    def test_filter_collisions(self):
        runs = load_tracker_runs()
        values = list(runs.run_class_name.unique())
        assert [
            "Cosmics18",
            "Commissioning18",
            "Collisions18",
            "Collisions18SpecialRun",
        ] == values

        collisions = filter_collisions(runs)
        assert ["Collisions18", "Collisions18SpecialRun"] == list(
            collisions.run_class_name.unique()
        )
        assert ["collisions"] == list(collisions.runtype.unique())

    def test_filter_cosmics(self):
        runs = load_tracker_runs()
        values = list(runs.run_class_name.unique())
        assert [
            "Cosmics18",
            "Commissioning18",
            "Collisions18",
            "Collisions18SpecialRun",
        ] == values

        cosmics = filter_cosmics(runs)
        assert ["Cosmics18"] == list(cosmics.run_class_name.unique())
        assert ["cosmics"] == list(cosmics.runtype.unique())

    def test_filter_prompt(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = filter_prompt(runs)
        assert ["prompt"] == list(filtered.reco.unique())

    def test_filter_express(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = filter_express(runs)
        assert ["express"] == list(filtered.reco.unique())

    def test_filter_rereco(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = filter_rereco(runs)
        assert ["rereco"] == list(filtered.reco.unique())

    def test_filter_online(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = filter_online(runs)
        assert ["online"] == list(filtered.reco.unique())

    def test_filter_lumisections(self):
        runs = load_tracker_runs()

        assert not runs.empty
        assert not runs[runs["lumisections"] < 30].empty

        runs = filter_lumisections_gte(runs, 30)

        assert not runs.empty
        assert runs[runs["lumisections"] < 30].empty


class TestExclude:
    def test_exclude_collisions(self):
        runs = load_tracker_runs()
        values = list(runs.run_class_name.unique())
        assert [
            "Cosmics18",
            "Commissioning18",
            "Collisions18",
            "Collisions18SpecialRun",
        ] == values

        collisions = exclude_collisions(runs)
        assert ["Cosmics18", "Commissioning18"] == list(
            collisions.run_class_name.unique()
        )

    def test_exclude_cosmics(self):
        runs = load_tracker_runs()
        values = list(runs.run_class_name.unique())
        assert [
            "Cosmics18",
            "Commissioning18",
            "Collisions18",
            "Collisions18SpecialRun",
        ] == values

        cosmics = exclude_cosmics(runs)
        assert ["Commissioning18", "Collisions18", "Collisions18SpecialRun"] == list(
            cosmics.run_class_name.unique()
        )

    def test_exclude_prompt(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = exclude_prompt(runs)
        assert ["express", "online", "rereco"] == list(filtered.reco.unique())

    def test_exclude_express(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = exclude_express(runs)
        assert ["online", "prompt", "rereco"] == list(filtered.reco.unique())

    def test_exclude_rereco(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = exclude_rereco(runs)
        assert ["express", "online", "prompt"] == list(filtered.reco.unique())

    def test_exclude_online(self):
        runs = load_tracker_runs()
        values = list(runs.reco.unique())
        assert ["express", "online", "prompt", "rereco"] == values

        filtered = exclude_online(runs)
        assert ["express", "prompt", "rereco"] == list(filtered.reco.unique())

    def test_exclude_lumisections(self):
        runs = load_tracker_runs()

        assert not runs.empty
        assert not runs[runs["lumisections"] >= 30].empty

        runs = runs.pipe(exclude_lumisections_gte, 30)

        assert not runs.empty
        assert runs[runs["lumisections"] >= 30].empty
