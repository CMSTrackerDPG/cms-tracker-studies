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


def unify_values(data_frame):
    data_frame.reco = data_frame.reco.str.lower()
    data_frame["reco"] = data_frame["reco"].replace(regex="promptreco", value="prompt")
    return data_frame
