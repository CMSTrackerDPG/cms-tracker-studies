import numpy
import pandas

from trackerstudies.filters import (
    exclude_online,
    exclude_commissioning,
    exclude_special,
)
from .merge import merge_runreg_tkdqmdoc, merge_runreg_oms
from .pipes import (
    add_runtype,
    add_is_bad,
    add_reference_cost,
    add_is_heavy_ion,
    add_is_commissioning,
    add_is_special,
)
from .algorithms import reference_cost
from .exceptions import TrackingMapNotFound
from .extract import extract_tracking_map_content
from .load import (
    load_tracking_map,
    load_tracker_runs,
    load_tkdqmdoctor_runs,
    load_oms_runs,
)


def calculate_tracking_map_reference_cost(run_number, reference_run_number, reco):
    try:
        tracking_map = load_tracking_map(run_number, reco)
        reference_map = load_tracking_map(reference_run_number, reco)
    except TrackingMapNotFound:
        # print("Cant find tracking map for {} {} ".format(row.run_number, row.reco))
        return numpy.nan
    except ValueError:
        # print("Incompatible Map for {} {} ".format(row.run_number, row.reco))
        return numpy.nan

    tracking_map_content = extract_tracking_map_content(tracking_map)
    reference_map_content = extract_tracking_map_content(reference_map)
    return reference_cost(tracking_map_content, reference_map_content)


def setup_pandas_display(max_rows=10, max_columns=10, width=1000):
    pandas.set_option("display.max_rows", max_rows)
    pandas.set_option("display.max_columns", max_columns)
    pandas.set_option("display.width", width)


def load_fully_setup_tracker_runs():
    tracker_runs = load_tracker_runs()
    tkdqmdoctor_runs = load_tkdqmdoctor_runs()
    oms_runs = load_oms_runs()

    return (
        tracker_runs.pipe(merge_runreg_tkdqmdoc, tkdqmdoctor_runs)
        .pipe(merge_runreg_oms, oms_runs)
        .pipe(exclude_online)
        .pipe(add_runtype)
        .pipe(add_is_bad)
        .pipe(add_reference_cost)
        .pipe(add_is_special)
        .pipe(add_is_commissioning)
        .pipe(add_is_heavy_ion)
        .pipe(exclude_commissioning)
        .pipe(exclude_special)
    )
