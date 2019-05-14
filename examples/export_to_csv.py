from trackerstudies.filters import filter_collisions
from trackerstudies.utils import load_runs

runs = load_runs()
runs.to_csv("data/data.csv")

collision_runs = runs.pipe(filter_collisions)
runs.to_csv("data/collision_data.csv")
