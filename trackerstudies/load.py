import json
import os

import pandas

from trackerstudies.exceptions import TrackingMapNotFound
from trackerstudies.merge import merge_runreg_runreg
from trackerstudies.pipes import unify_columns, unify_values

DATA_DIRECTORY = "data"
TRACKING_MAP_DIRECTORY = "TrackEtaPhi_ImpactPoint_GenTk"


def load_tracking_map(run_number, reco):
    file_name = "{}_{}.json".format(run_number, reco.lower())
    path = os.path.join(DATA_DIRECTORY, TRACKING_MAP_DIRECTORY, file_name)
    try:
        with open(path) as file:
            return json.load(file)
    except FileNotFoundError:
        raise TrackingMapNotFound(
            "Unable to load tracking map for run {} ({}). "
            "File '{}' does not exist.".format(run_number, reco, path)
        )


def load_json_as_pandas(file_name):
    """
    :param file_name: output file of runregcrawlr
    :return: pandas dataframe
    """
    with open(file_name) as file:
        return pandas.read_json(file)


def load_run_registry_json(workspace):
    """
    Loads the runregcrawlr-{workspace}-output.json file provided by the runregcrawlr

    :param workspace: workspace name e.g. 'tracker' or 'global'
    :return: pandas dataframe
    """

    filename = "runregcrawlr-{}-output.json".format(workspace)
    path = os.path.join(DATA_DIRECTORY, filename)
    return load_json_as_pandas(path)


def load_tracker_runs():
    return load_run_registry_json("tracker").pipe(unify_columns).pipe(unify_values)


def load_global_runs():
    return load_run_registry_json("global").pipe(unify_columns).pipe(unify_values)


def load_all_runreg_runs():
    tracker_runs = load_tracker_runs()
    global_runs = load_global_runs()
    return merge_runreg_runreg(tracker_runs, global_runs)


def load_oms_json():
    filename = "oms_runs.json"
    path = os.path.join(DATA_DIRECTORY, filename)
    return load_json_as_pandas(path)


def load_oms_runs():
    return load_oms_json()


def load_oms_fills():
    raise NotImplementedError


def load_tkdqmdoctor_runs_json(filename):
    runs = load_json_as_pandas(filename).rename(
        columns={
            "type__reco": "reco",
            "reference_run__reference_run": "reference_run_number",
        }
    )
    runs.reco = runs.reco.str.lower()
    return runs


def load_tkdqmdoctor_runs():
    filename = "tkdqmdoc.json"
    path = os.path.join(DATA_DIRECTORY, filename)
    return load_tkdqmdoctor_runs_json(path)


def load_tkdqmdoc_problematic_runs():
    filename = "tkdqmdoctor_problems.json"
    path = os.path.join(DATA_DIRECTORY, filename)
    return load_tkdqmdoctor_runs_json(path)
