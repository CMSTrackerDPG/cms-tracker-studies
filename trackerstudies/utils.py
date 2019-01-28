import numpy

from .algorithms import reference_cost
from .exceptions import TrackingMapNotFound
from .extract import extract_tracking_map_content
from .load import load_tracking_map


def calculate_tracking_map_reference_cost(run_number, reference_run_number, reco):
    tracking_map = load_tracking_map(run_number, reco)
    reference_map = load_tracking_map(reference_run_number, reco)

    try:
        tracking_map_content = extract_tracking_map_content(tracking_map)
        reference_map_content = extract_tracking_map_content(reference_map)
    except TrackingMapNotFound:
        # print("Cant find tracking map for {} {} ".format(row.run_number, row.reco))
        return numpy.nan
    except ValueError:
        # print("Incompatible Map for {} {} ".format(row.run_number, row.reco))
        return numpy.nan

    return reference_cost(tracking_map_content, reference_map_content)
