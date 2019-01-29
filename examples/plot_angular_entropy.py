from trackerstudies.filters import filter_run_number_range, filter_collisions
from trackerstudies.pipes import add_angular_entropy
from trackerstudies.plots import plot_angular_entropy
from trackerstudies.utils import load_fully_setup_tracker_runs

runs = (
    load_fully_setup_tracker_runs()
    .pipe(filter_collisions)
    .pipe(filter_run_number_range, 317400, 317500)
    .pipe(add_angular_entropy)
)

plot_angular_entropy(runs, show=True, save=True)
