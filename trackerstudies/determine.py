import numpy


def determine_tracker_is_bad(pixel, strip, tracking, runtype):
    return (
        pixel.lower() != "good"
        and runtype.lower() == "collisions"
        or strip.lower() != "good"
        or tracking.lower() != "good"
    )


def determine_is_collisions(run_class_name, rda_name):
    return "Collisions" in run_class_name or "Collisions" in rda_name


def determine_is_cosmics(run_class_name, rda_name):
    return "Collisions" in run_class_name or "Collisions" in rda_name


def determine_run_type(run_class_name, rda_name):
    return (
        "collisions"
        if determine_is_collisions(run_class_name, rda_name)
        else "cosmics"
        if determine_is_cosmics(run_class_name, rda_name)
        else numpy.nan
    )
