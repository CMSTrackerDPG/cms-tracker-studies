from trackerstudies.plots import plot_tracking_map

# Show a Tracking and save as "yourname.png"
plot_tracking_map(321755, "Express", show=True, save="yourname.png")

# Show a Tracking and save as "tracking_map_321126_Prompt.pdf
plot_tracking_map(321126, "Prompt", show=True, save=True)

# Dont show the Tracking, but save as "tracking_map_321140_Prompt.pdf
plot_tracking_map(321140, "Prompt", save=True)
