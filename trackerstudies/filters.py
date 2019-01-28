#########
# Filter
#########
from .pipes import add_runtype


def _filter_reco(dataframe, value):
    return dataframe[dataframe.reco == value]


def _filter_runtype(dataframe, value):
    try:
        return dataframe[dataframe.runtype == value]
    except AttributeError:
        dataframe = dataframe.pipe(add_runtype)
        return dataframe[dataframe.runtype == value]


def filter_prompt(dataframe):
    return dataframe.pipe(_filter_reco, "prompt")


def filter_express(dataframe):
    return dataframe.pipe(_filter_reco, "express")


def filter_rereco(dataframe):
    return dataframe.pipe(_filter_reco, "rereco")


def filter_online(dataframe):
    return dataframe.pipe(_filter_reco, "online")


def filter_collisions(dataframe):
    return dataframe.pipe(_filter_runtype, "collisions")


def filter_cosmics(dataframe):
    return dataframe.pipe(_filter_runtype, "cosmics")


def filter_heavy_ion(dataframe):
    return dataframe[dataframe.heavy_ion]


def filter_commissioning(dataframe):
    return dataframe[dataframe.commissioning]


def filter_special(dataframe):
    raise NotImplementedError


def filter_lumisections_gte(dataframe, lumisections):
    return dataframe[dataframe["lumisections"] > lumisections]


##########
# Exclude
##########


def _exclude_reco(dataframe, value):
    return dataframe[dataframe.reco != value]


def _exclude_runtype(dataframe, value):
    try:
        return dataframe[dataframe.runtype != value]
    except AttributeError:
        dataframe = dataframe.pipe(add_runtype)
        return dataframe[dataframe.runtype != value]


def exclude_prompt(dataframe):
    return dataframe.pipe(_exclude_reco, "prompt")


def exclude_express(dataframe):
    return dataframe.pipe(_exclude_reco, "express")


def exclude_rereco(dataframe):
    return dataframe.pipe(_exclude_reco, "rereco")


def exclude_online(dataframe):
    return dataframe.pipe(_exclude_reco, "online")


def exclude_collisions(dataframe):
    return dataframe.pipe(_exclude_runtype, "collisions")


def exclude_cosmics(dataframe):
    return dataframe.pipe(_exclude_runtype, "cosmics")


def exclude_heavy_ion(dataframe):
    return dataframe[~dataframe.heavy_ion]


def exclude_commissioning(dataframe):
    return dataframe[~dataframe.commissioning]


def exclude_special(dataframe):
    raise NotImplementedError


def exclude_lumisections_gte(dataframe, lumisections):
    return dataframe[dataframe["lumisections"] < lumisections]
