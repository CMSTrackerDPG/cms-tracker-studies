from .determine import (
    determine_runtype,
    determine_tracker_is_bad,
    determine_is_heavy_ion,
    determine_is_commissioning,
    determine_is_special,
)


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
        lambda row: determine_runtype(row.run_class_name), axis=1
    )

    return dataframe


def add_is_bad(df):
    if "runtype" not in df:
        add_runtype(df)
    df.loc[:, "is_bad"] = df.apply(
        lambda row: determine_tracker_is_bad(
            row.pixel, row.strip, row.tracking, row.runtype
        ),
        axis=1,
    )
    return df


def add_reference_cost(dataframe):
    from .utils import calculate_tracking_map_reference_cost

    dataframe.loc[:, "reference_cost"] = dataframe.apply(
        lambda row: calculate_tracking_map_reference_cost(
            row.run_number, row.reference_run_number, row.reco
        ),
        axis=1,
    )
    return dataframe


def add_is_reference_run(dataframe):
    raise NotImplementedError


def add_is_heavy_ion(dataframe):
    dataframe.loc[:, "is_heavy_ion"] = dataframe.apply(
        lambda row: determine_is_heavy_ion(row.rda_name), axis=1
    )
    return dataframe


def add_is_commissioning(dataframe):
    dataframe.loc[:, "is_commissioning"] = dataframe.apply(
        lambda row: determine_is_commissioning(row.run_class_name, row.rda_name), axis=1
    )

    dataframe.loc[
        dataframe.run_number.isin(
            dataframe[dataframe["is_commissioning"]].run_number.unique()
        ),
        "is_commissioning",
    ] = True
    return dataframe


def add_is_special(dataframe):
    dataframe.loc[:, "is_special"] = dataframe.apply(
        lambda row: determine_is_special(row.run_class_name, row.rda_name), axis=1
    )
    return dataframe
