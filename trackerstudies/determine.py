import numpy


def determine_tracker_is_bad(pixel, strip, tracking, runtype):
    try:
        return (
            pixel.lower() != "good"
            and runtype.lower() == "collisions"
            or strip.lower() != "good"
            or tracking.lower() != "good"
        )
    except AttributeError:
        return numpy.nan


def determine_is_heavy_ion(rda_name):
    return "HI" in rda_name


def determine_is_commissioning(run_class_name, rda_name):
    return "Commissioning" in run_class_name or "Commiss" in rda_name


def determine_is_special(run_class_name, rda_name):
    return "Special" in run_class_name or "Special" in rda_name


def determine_is_collisions(run_class_name):
    return "Collisions" in run_class_name


def determine_is_cosmics(run_class_name):
    return "Cosmics" in run_class_name


def determine_runtype(run_class_name):
    return (
        "collisions"
        if determine_is_collisions(run_class_name)
        else "cosmics"
        if determine_is_cosmics(run_class_name)
        else numpy.nan
    )
