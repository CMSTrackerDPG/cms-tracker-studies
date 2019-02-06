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


def determine_has_problem(problem_names, comment, problem_string):
    if any(problem_string in problem.lower() for problem in problem_names):
        return True
    if problem_string in comment.lower():
        return True
    return False


def determine_has_fed_error(problem_names, comment):
    return determine_has_problem(problem_names, comment, "fed error")


def determine_has_dcs_error(problem_names, comment):
    return determine_has_problem(problem_names, comment, "dcs error")


def determine_has_new_hole(problem_names, comment):
    return determine_has_problem(problem_names, comment, "new hole")


def determine_has_dead_channel(problem_names, comment):
    return determine_has_problem(problem_names, comment, "dead channel")


def determine_has_low_signal_noise(problem_names, comment):
    return determine_has_problem(problem_names, comment, "low s/n")


def determine_has_noisy_module(problem_names, comment):
    return determine_has_problem(problem_names, comment, "noisy module")


def determine_has_power_supply_problem(problem_names, comment):
    return determine_has_problem(problem_names, comment, "ps problem")


def determine_has_low_cluster_charge(problem_names, comment):
    return determine_has_problem(problem_names, comment, "low cluster charge")


def determine_has_many_bad_components(problem_names, comment):
    return determine_has_problem(
        problem_names, comment, "large number of bad component"
    )


def determine_has_trigger_problem(problem_names, comment):
    return determine_has_problem(problem_names, comment, "trigger issue")
