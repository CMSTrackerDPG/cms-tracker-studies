library(tidyverse)

# Read the data
data <- read_csv("data/data.csv")

# Manipulate data
data$tracking <- factor(data$tracking, levels=c("GOOD", "BAD"))
data <- data %>% filter(runtype=='collisions')
data <- data %>% arrange(tracking)
data <- data %>% filter(Hits.Pixel.mean > 0) %>% filter(Hits.Strip.mean > 0)

# Create plots
data %>%
  filter(fill__era %in%  c("2018B", "2018D")) %>%
  ggplot(aes(clusters.OnTrack.TIB.rms, clusters.OffTrack.TIB.rms ,colour=reco)) +
  geom_point() +
  facet_grid(. ~ fill__era) +
  scale_color_brewer(palette="Dark2")
ggsave("images/clusters_reco.png", width = 8, height=6)


data %>%
  filter(fill__era %in%  c("2018B", "2018D")) %>%
  ggplot(aes(clusters.OnTrack.TIB.rms, clusters.OffTrack.TIB.rms ,colour=tracking)) +
  geom_point() +
  facet_grid(. ~ fill__era) +
  scale_color_brewer(palette="Dark2")
ggsave("images/clusters_tracking.png", width = 8, height=6)
