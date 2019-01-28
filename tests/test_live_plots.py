from tests.conftest import SHOW_PLOTS
from trackerstudies.plots import plot_tracking_map


def test_plot_tracking_map():
    run_number = 321755
    reco = "Express"
    plot_tracking_map(run_number, reco, show=SHOW_PLOTS)
