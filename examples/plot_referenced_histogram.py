from trackerstudies.plots import plot_referenced_tracking_map_histogram

run_number = 317512
reference_run_number = 317435
reco = "Prompt"
title = "Pixel is Bad"
plot_referenced_tracking_map_histogram(
    run_number, reference_run_number, reco, title=title, show=True
)

run_number = 317435
reference_run_number = 317435
reco = "Prompt"
title = "Reference against itself"
plot_referenced_tracking_map_histogram(
    run_number, reference_run_number, reco, title=title, show=True
)

run_number = 322483
reference_run_number = 321755
reco = "Prompt"
title = "Very noisy run"
plot_referenced_tracking_map_histogram(
    run_number, reference_run_number, reco, title=title, show=True
)

run_number = 322492
reference_run_number = 321755
reco = "Prompt"
title = "Good run"
plot_referenced_tracking_map_histogram(
    run_number, reference_run_number, reco, title=title, show=True
)
