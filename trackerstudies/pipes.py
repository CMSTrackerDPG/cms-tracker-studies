import numpy


def _unify_column_names(column_names):
    new_names = []
    for c in column_names:
        if c.endswith("rda_cmp_pix") or c.startswith("rda_cmp_pix_"):
            new_names.append(c.replace("pix", "pixel"))
        elif c.endswith("rda_cmp_track") or c.startswith("rda_cmp_track_"):
            new_names.append(c.replace("track", "tracking"))
        elif c == "rda_wor_name":
            new_names.append("workspace")
        else:
            new_names.append(c)
    return new_names


def _remove_prefix(items, prefix):
    return [item.replace(prefix, "") for item in items]


def unify_columns(data_frame):
    column_names = list(data_frame)
    new_names = _unify_column_names(column_names)
    new_names = _remove_prefix(new_names, "rda_cmp_")
    data_frame.columns = new_names
    return data_frame


def unify_values(dataframe):
    dataframe.reco = dataframe.reco.str.lower()
    dataframe["reco"] = dataframe["reco"].replace(regex="promptreco", value="prompt")
    return dataframe


def determine_run_type(row):
    if "Collisions" in row["run_class_name"] or "Collisions" in row["rda_name"]:
        return "collisions"
    if "Cosmics" in row["run_class_name"] or "Cosmics" in row["rda_name"]:
        return "cosmics"
    return numpy.nan


def add_runtype(dataframe):
    # Handle obvious cases
    dataframe["runtype"] = dataframe.apply(determine_run_type, axis=1)

    # Handle missing cases
    from trackerstudies.filters import filter_collisions, filter_cosmics

    collisions_run_numbers = dataframe.pipe(filter_collisions).run_number.unique()
    cosmics_run_numbers = dataframe.pipe(filter_cosmics).run_number.unique()

    dataframe.loc[
        dataframe.run_number.isin(collisions_run_numbers), "runtype"
    ] = "collisions"
    dataframe.loc[dataframe.run_number.isin(cosmics_run_numbers), "runtype"] = "cosmics"

    return dataframe
