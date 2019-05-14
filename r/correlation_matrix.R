library(tidyverse)
library(corrplot)
library(corrr)
source("r/scripts.R")

# Read the data
data <- read_csv("data/data.csv")

# Manipulate data
data$tracking <- factor(data$tracking, levels=c("GOOD", "BAD"))
data <- data %>%
  filter(runtype=='collisions') %>%
  filter(Hits.Pixel.mean > 0) %>%
  filter(Hits.Strip.mean > 0) %>%
  arrange(tracking)

# Exclude heavy ion runs
protons <- data %>%
  filter(fill__era != "HIRun2018A", reco %in% c('express', 'prompt')) %>%
  filter(Hits.Pixel.mean > 0) %>%
  filter(Hits.Strip.mean > 0)

# All proton collisions runs that were certified good
protons_good <- protons %>%
  filter(tracking=="GOOD")

# All proton collisions runs that were certified bad
protons_bad <- protons %>%
  filter(tracking=="BAD")

# Use only the feature columns
protons_features <- protons %>%
  select(contains(".rms"),contains(".mean"),contains(".entries"),contains(".integral"))

protons_good_features <- protons_good %>%
  select(contains(".rms"),contains(".mean"),contains(".entries"),contains(".integral"))

protons_good_features_corr <- protons_good_features %>%
  correlate() %>%
  stretch()

protons_features_corr <- protons_features %>%
  correlate() %>%
  stretch()

my_df <- protons_features_corr
my_df$r_good <- protons_good_features_corr$r
my_df <- my_df %>% mutate(subtracted = r_good - r)

# Filter to all runs with very high correlation for good runs
# and noticeably less correlation for bad runs
tmp <- my_df %>% filter(r_good > 0.95, r < 0.85)

# Use only a subset of features to make it easier to display
corr_loss_columns <- c(
  'Seeds.mixedTriplet.rms', 'Seeds.pixelLess.rms', 'Seeds.tobTec.rms',
  'Tracks.rms', 'clusters.OnTrack.TIB.rms', 'clusters.OnTrack.TOB.rms',
  'clusters.OnTrack.TID.PLUS.rms', 'clusters.OffTrack.TIB.rms', 'clusters.OffTrack.TID.MINUS.rms',
  'Seeds.mixedTriplet.mean', 'Seeds.pixelLess.mean', 'Seeds.tobTec.mean',
  'Tracks.mean', 'digis.PXBarrel.mean', 'digis.PXForward.mean',
  'clusters.PXBarrel.mean', 'clusters.PXForward.mean',
  'clusters.OnTrack.TIB.mean', 'clusters.OnTrack.TID.MINUS.mean')

protons %>% select(corr_loss_columns) %>%
  rename("RMS of mixedTriplet seeds" = "Seeds.mixedTriplet.rms") %>%
  rename("RMS of pixelLess seeds" = "Seeds.pixelLess.rms") %>%
  rename("RMS of tobTec seeds" = "Seeds.tobTec.rms") %>%
  rename("RMS of number of Tracks" = "Tracks.rms") %>%
  rename("RMS of OnTrack clusters TIB" = "clusters.OnTrack.TIB.rms") %>%
  rename("RMS of OnTrack clusters TOB" = "clusters.OnTrack.TOB.rms") %>%
  rename("RMS of OnTrack clusters TTD PLUS" = "clusters.OnTrack.TID.PLUS.rms") %>%
  rename("RMS of OffTrack clusters TIB" = "clusters.OffTrack.TIB.rms") %>%
  rename("RMS of OffTrack clusters TID MINUS" = "clusters.OffTrack.TID.MINUS.rms") %>%
  rename("Mean number of mixedtriplet Seeds" = "Seeds.mixedTriplet.mean") %>%
  rename("Mean number of pixelLess seeds" = "Seeds.pixelLess.mean") %>%
  rename("Mean number of tobTec seeds" = "Seeds.tobTec.mean") %>%
  rename("Mean number of Tracks" = "Tracks.mean") %>%
  rename("Mean number of digis PXBarrel" = "digis.PXBarrel.mean") %>%
  rename("Mean number of digis PXForward" = "digis.PXForward.mean") %>%
  rename("Mean number of clusters PXBarrel" = "clusters.PXBarrel.mean") %>%
  rename("Mean number of clusters PXForward" = "clusters.PXForward.mean") %>%
  rename("Mean number of clusters OnTrack TIB" = "clusters.OnTrack.TIB.mean") %>%
  rename("Mean number of clusters OnTrack TID MINUS" = "clusters.OnTrack.TID.MINUS.mean") %>%
  correlate() %>% rplot()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(fill="correlation loss", colour="Correlation") +
  ggtitle("Pearson correlation coefficient of all runs")
ggsave("images/correlation_all.png", width=10, height=9)
ggsave("images/correlation_all.pdf", width=10, height=9)

protons_good %>% select(corr_loss_columns) %>%
  rename("RMS of mixedTriplet seeds" = "Seeds.mixedTriplet.rms") %>%
  rename("RMS of pixelLess seeds" = "Seeds.pixelLess.rms") %>%
  rename("RMS of tobTec seeds" = "Seeds.tobTec.rms") %>%
  rename("RMS of number of Tracks" = "Tracks.rms") %>%
  rename("RMS of OnTrack clusters TIB" = "clusters.OnTrack.TIB.rms") %>%
  rename("RMS of OnTrack clusters TOB" = "clusters.OnTrack.TOB.rms") %>%
  rename("RMS of OnTrack clusters TTD PLUS" = "clusters.OnTrack.TID.PLUS.rms") %>%
  rename("RMS of OffTrack clusters TIB" = "clusters.OffTrack.TIB.rms") %>%
  rename("RMS of OffTrack clusters TID MINUS" = "clusters.OffTrack.TID.MINUS.rms") %>%
  rename("Mean number of mixedtriplet Seeds" = "Seeds.mixedTriplet.mean") %>%
  rename("Mean number of pixelLess seeds" = "Seeds.pixelLess.mean") %>%
  rename("Mean number of tobTec seeds" = "Seeds.tobTec.mean") %>%
  rename("Mean number of Tracks" = "Tracks.mean") %>%
  rename("Mean number of digis PXBarrel" = "digis.PXBarrel.mean") %>%
  rename("Mean number of digis PXForward" = "digis.PXForward.mean") %>%
  rename("Mean number of clusters PXBarrel" = "clusters.PXBarrel.mean") %>%
  rename("Mean number of clusters PXForward" = "clusters.PXForward.mean") %>%
  rename("Mean number of clusters OnTrack TIB" = "clusters.OnTrack.TIB.mean") %>%
  rename("Mean number of clusters OnTrack TID MINUS" = "clusters.OnTrack.TID.MINUS.mean") %>%
  correlate() %>% rplot() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(fill="correlation loss", colour="Correlation") +
  ggtitle("Pearson correlation coefficient of good runs")
ggsave("images/correlation_good.png", width=10, height=9)
ggsave("images/correlation_good.pdf", width=10, height=9)

protons_bad %>% select(corr_loss_columns) %>%
  rename("RMS of mixedTriplet seeds" = "Seeds.mixedTriplet.rms") %>%
  rename("RMS of pixelLess seeds" = "Seeds.pixelLess.rms") %>%
  rename("RMS of tobTec seeds" = "Seeds.tobTec.rms") %>%
  rename("RMS of number of Tracks" = "Tracks.rms") %>%
  rename("RMS of OnTrack clusters TIB" = "clusters.OnTrack.TIB.rms") %>%
  rename("RMS of OnTrack clusters TOB" = "clusters.OnTrack.TOB.rms") %>%
  rename("RMS of OnTrack clusters TTD PLUS" = "clusters.OnTrack.TID.PLUS.rms") %>%
  rename("RMS of OffTrack clusters TIB" = "clusters.OffTrack.TIB.rms") %>%
  rename("RMS of OffTrack clusters TID MINUS" = "clusters.OffTrack.TID.MINUS.rms") %>%
  rename("Mean number of mixedtriplet Seeds" = "Seeds.mixedTriplet.mean") %>%
  rename("Mean number of pixelLess seeds" = "Seeds.pixelLess.mean") %>%
  rename("Mean number of tobTec seeds" = "Seeds.tobTec.mean") %>%
  rename("Mean number of Tracks" = "Tracks.mean") %>%
  rename("Mean number of digis PXBarrel" = "digis.PXBarrel.mean") %>%
  rename("Mean number of digis PXForward" = "digis.PXForward.mean") %>%
  rename("Mean number of clusters PXBarrel" = "clusters.PXBarrel.mean") %>%
  rename("Mean number of clusters PXForward" = "clusters.PXForward.mean") %>%
  rename("Mean number of clusters OnTrack TIB" = "clusters.OnTrack.TIB.mean") %>%
  rename("Mean number of clusters OnTrack TID MINUS" = "clusters.OnTrack.TID.MINUS.mean") %>%
  correlate() %>% rplot() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  labs(fill="correlation loss", colour="Correlation") +
  ggtitle("Pearson correlation coefficient of bad runs")
ggsave("images/correlation_bad.png", width=10, height=9)
ggsave("images/correlation_bad.pdf", width=10, height=9)

tmp %>%
  mutate(x = replace(x, x == "Seeds.mixedTriplet.rms", "RMS of mixedTriplet seeds")) %>%
  mutate(x = replace(x, x == "Seeds.pixelLess.rms", "RMS of pixelLess seeds")) %>%
  mutate(x = replace(x, x == "Seeds.tobTec.rms", "RMS of tobTec seeds")) %>%
  mutate(x = replace(x, x == "Tracks.rms", "RMS of number of Tracks" )) %>%
  mutate(x = replace(x, x == "clusters.OnTrack.TIB.rms", "RMS of OnTrack clusters TIB" )) %>%
  mutate(x = replace(x, x == "clusters.OnTrack.TOB.rms", "RMS of OnTrack clusters TOB" )) %>%
  mutate(x = replace(x, x == "clusters.OnTrack.TID.PLUS.rms", "RMS of OnTrack clusters TTD PLUS")) %>%
  mutate(x = replace(x, x == "clusters.OffTrack.TIB.rms", "RMS of OffTrack clusters TIB" )) %>%
  mutate(x = replace(x, x == "clusters.OffTrack.TID.MINUS.rms", "RMS of OffTrack clusters TID MINUS" )) %>%
  mutate(x = replace(x, x == "Seeds.mixedTriplet.mean", "Mean number of mixedtriplet Seeds" )) %>%
  mutate(x = replace(x, x == "Seeds.pixelLess.mean", "Mean number of pixelLess seeds" )) %>%
  mutate(x = replace(x, x == "Seeds.tobTec.mean", "Mean number of tobTec seeds" )) %>%
  mutate(x = replace(x, x == "Tracks.mean", "Mean number of Tracks" )) %>%
  mutate(x = replace(x, x == "digis.PXBarrel.mean", "Mean number of digis PXBarrel" )) %>%
  mutate(x = replace(x, x == "digis.PXForward.mean", "Mean number of digis PXForward" )) %>%
  mutate(x = replace(x, x == "clusters.PXBarrel.mean", "Mean number of clusters PXBarrel" )) %>%
  mutate(x = replace(x, x == "clusters.PXForward.mean", "Mean number of clusters PXForward")) %>%
  mutate(x = replace(x, x == "clusters.OnTrack.TIB.mean", "Mean number of clusters OnTrack TIB")) %>%
  mutate(x = replace(x, x == "clusters.OnTrack.TID.MINUS.mean", "Mean number of clusters OnTrack TID MINUS" )) %>%
  mutate(y = replace(y, y == "Seeds.mixedTriplet.rms", "RMS of mixedTriplet seeds")) %>%
  mutate(y = replace(y, y == "Seeds.pixelLess.rms", "RMS of pixelLess seeds")) %>%
  mutate(y = replace(y, y == "Seeds.tobTec.rms", "RMS of tobTec seeds")) %>%
  mutate(y = replace(y, y == "Tracks.rms", "RMS of number of Tracks" )) %>%
  mutate(y = replace(y, y == "clusters.OnTrack.TIB.rms", "RMS of OnTrack clusters TIB" )) %>%
  mutate(y = replace(y, y == "clusters.OnTrack.TOB.rms", "RMS of OnTrack clusters TOB" )) %>%
  mutate(y = replace(y, y == "clusters.OnTrack.TID.PLUS.rms", "RMS of OnTrack clusters TTD PLUS")) %>%
  mutate(y = replace(y, y == "clusters.OffTrack.TIB.rms", "RMS of OffTrack clusters TIB" )) %>%
  mutate(y = replace(y, y == "clusters.OffTrack.TID.MINUS.rms", "RMS of OffTrack clusters TID MINUS" )) %>%
  mutate(y = replace(y, y == "Seeds.mixedTriplet.mean", "Mean number of mixedtriplet Seeds" )) %>%
  mutate(y = replace(y, y == "Seeds.pixelLess.mean", "Mean number of pixelLess seeds" )) %>%
  mutate(y = replace(y, y == "Seeds.tobTec.mean", "Mean number of tobTec seeds" )) %>%
  mutate(y = replace(y, y == "Tracks.mean", "Mean number of Tracks" )) %>%
  mutate(y = replace(y, y == "digis.PXBarrel.mean", "Mean number of digis PXBarrel" )) %>%
  mutate(y = replace(y, y == "digis.PXForward.mean", "Mean number of digis PXForward" )) %>%
  mutate(y = replace(y, y == "clusters.PXBarrel.mean", "Mean number of clusters PXBarrel" )) %>%
  mutate(y = replace(y, y == "clusters.PXForward.mean", "Mean number of clusters PXForward")) %>%
  mutate(y = replace(y, y == "clusters.OnTrack.TIB.mean", "Mean number of clusters OnTrack TIB")) %>%
  mutate(y = replace(y, y == "clusters.OnTrack.TID.MINUS.mean", "Mean number of clusters OnTrack TID MINUS" )) %>%
  ggplot(aes(x, y, fill=subtracted, label=round(r, 1))) +
  geom_tile() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  xlab("") +
  ylab("") +
  labs(fill="correlation loss") +
  scale_fill_gradient2(mid="white", high="orangered", limits=c(0, 1)) +
  ggtitle("Pearson correlation coefficient loss between good and bad runs")
ggsave("images/correlation_loss.png", width=10, height=9)
ggsave("images/correlation_loss.pdf", width=10, height=9)