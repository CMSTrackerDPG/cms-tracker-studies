from .determine import determine_run_type, determine_tracker_is_bad


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


def add_runtype(dataframe):
    # Handle obvious cases
    dataframe["runtype"] = dataframe.apply(
        lambda row: determine_run_type(row.run_class_name, row.rda_name), axis=1
    )

    # Handle missing cases
    from trackerstudies.filters import filter_collisions, filter_cosmics

    collisions_run_numbers = dataframe.pipe(filter_collisions).run_number.unique()
    cosmics_run_numbers = dataframe.pipe(filter_cosmics).run_number.unique()

    dataframe.loc[
        dataframe.run_number.isin(collisions_run_numbers), "runtype"
    ] = "collisions"
    dataframe.loc[dataframe.run_number.isin(cosmics_run_numbers), "runtype"] = "cosmics"

    return dataframe


def add_is_bad(df):
    if "runtype" not in df:
        add_runtype(df)
    df.loc[:, "is_bad"] = df.apply(
        lambda row: determine_tracker_is_bad(row.pixel, row.strip, row.tracking, row.runtype),
        axis=1,
    )
    return df


def add_reference_cost(dataframe):
    from .utils import calculate_tracking_map_reference_cost

    dataframe.loc[:, "cost"] = dataframe.apply(
        lambda row: calculate_tracking_map_reference_cost(
            row.run_number, row.reference_run_number, row.reco
        ),
        axis=1,
    )
    return dataframe
