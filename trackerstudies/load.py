import json
import os

import pandas

from .exceptions import TrackingMapNotFound
from .merge import merge_runreg_runreg
from .pipes import unify_columns, unify_values

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
            "type__beamtype": "beamtype",
            "type__beamenergy": "beamenergy",
            "type__dataset": "dataset",
            "reference_run__reference_run": "reference_run_number",
            "reference_run__reco": "reference_reco",
            "reference_run__runtype": "reference_runtype",
            "reference_run__beamtype": "reference_beamtype",
            "reference_run__beamenergy": "reference_beamenergy",
            "reference_run__dataset": "reference_dataset",
            "data": "certification_date",
        }
    )
    runs.reco = runs.reco.str.lower()
    runs.reference_run_number = runs.reference_run_number.astype(pandas.Int64Dtype())
    return runs


def load_tkdqmdoctor_runs():
    filename = "tkdqmdoctor_runs.json"
    path = os.path.join(DATA_DIRECTORY, filename)
    return load_tkdqmdoctor_runs_json(path)


def load_tkdqmdoctor_problem_runs():
    filename = "tkdqmdoctor_problem_runs.json"
    path = os.path.join(DATA_DIRECTORY, filename)
    return load_tkdqmdoctor_runs_json(path)


def read_histogram_folder(folder_name, attribute_prefix=None):
    folder = os.path.join("data", folder_name)
    file_names = sorted(os.listdir(folder))

    if not attribute_prefix:
        attribute_prefix = folder_name

    attributes = ["rms", "mean", "entries", "integral"]
    attributes = [
        "{}.{}".format(attribute_prefix, attribute) for attribute in attributes
    ]
    columns = ["run_number", "reco", *attributes]

    dataframe = pandas.DataFrame(columns=columns)
    dataframe.set_index(["run_number", "reco"], inplace=True)

    for file_name in file_names:
        run_number, reco = tuple(file_name.replace(".json", "").split("_"))
        run_number = int(run_number)
        path = os.path.join(folder, file_name)
        with open(path) as file:
            histogram = json.load(file)
            rms = histogram["hist"]["stats"]["rms"]["X"]["value"]
            mean = histogram["hist"]["stats"]["mean"]["X"]["value"]
            entries = histogram["hist"]["stats"]["entries"]
            integral = histogram["hist"]["bins"]["integral"]

            dataframe.loc[(run_number, reco), :] = [rms, mean, entries, integral]

    return dataframe


def load_all_histogram_folders(from_pickle=True):
    pickle_path = os.path.join("data", "histograms.pkl")
    try:
        if from_pickle:
            return pandas.read_pickle(pickle_path)
    except FileNotFoundError:
        pass
    prefixes = {
        "Chi2oNDF_GenTk": "Chi2oNDF",
        "NumberOfRecHitsPerTrack_GenTk": "Hits",
        "NumberOfRecHitsPerTrack_Pixel_GenTk": "Hits.Pixel",
        "NumberOfRecHitsPerTrack_Strip_GenTk": "Hits.Strip",
        "NumberOfSeeds_detachedTripletStepSeeds_detachedTripletStep": "Seeds.detachedTriplet",
        "NumberOfSeeds_initialStepSeeds_initialStep": "Seeds.initialStep",
        "NumberOfSeeds_lowPtTripletStepSeeds_lowPtTripletStep": "Seeds.lowPtTriplet",
        "NumberOfSeeds_mixedTripletStepSeeds_mixedTripletStep": "Seeds.mixedTriplet",
        "NumberOfSeeds_pixelLessStepSeeds_pixelLessStep": "Seeds.pixelLess",
        "NumberOfSeeds_pixelPairStepSeeds_pixelPairStep": "Seeds.pixelPair",
        "NumberOfSeeds_tobTecStepSeeds_tobTecStep": "Seeds.tobTec",
        "NumberOfTracks_GenTk": "Tracks",
        "TrackEta_ImpactPoint_GenTk": "TrackEta",
        "TrackPhi_ImpactPoint_GenTk": "TrackPhi",
        "TrackPt_ImpactPoint_GenTk": "TrackPt",
    }

    dataframe = pandas.DataFrame(columns=["run_number", "reco"])
    dataframe.set_index(["run_number", "reco"], inplace=True)

    for folder, prefix in prefixes.items():
        new_dataframe = read_histogram_folder(folder, prefix)
        dataframe = pandas.merge(
            dataframe, new_dataframe, left_index=True, right_index=True, how="outer"
        )

    dataframe.to_pickle(pickle_path)
    return dataframe
