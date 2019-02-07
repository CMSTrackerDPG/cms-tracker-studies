import matplotlib.pyplot as plt
import numpy

from trackerstudies.exceptions import TrackingMapNotFound
from trackerstudies.plots import plot_tracking_maps_side_by_side
from trackerstudies.utils import setup_pandas_display, load_runs

print("Loading runs...")
runs = load_runs()

setup_pandas_display(max_rows=50)

runs = runs[~runs.reference_run_number.isnull()]

print("Iterating...")
for index, row in runs.iterrows():
    run_number = row.run_number
    reco = row.reco
    reference_run_number = row.reference_run_number
    is_bad = row.is_bad

    lumis = numpy.around(row.recorded_lumi, decimals=1)

    subtitle = r"{} $ls$, {} ${}$".format(
        row.lumisections, lumis, row.recorded_lumi_unit
    )

    print("{} {} {} {} {}".format(run_number, reco, reference_run_number, is_bad,
                                  subtitle))

    try:
        plot_tracking_maps_side_by_side(
            run_number,
            reference_run_number,
            reco,
            subtitle=subtitle,
            subdir="{}/{}".format(reco, is_bad),
            is_bad=is_bad,
        )
        plt.clear()
        plt.close()
    except TrackingMapNotFound as e:
        print("ERROR:")
        print(e)
        pass
    except RecursionError as e:
        print("!! RecursionError:")
        print(e)
        exit()

# TODO choose previous run or previous good run instead of reference run
