library(tidyverse)

# Read the data
data <- read_csv("data/data.csv")

# Manipulate data
data$tracking <- factor(data$tracking, levels=c("GOOD", "BAD"))
data <- data %>% filter(runtype=='collisions')
data <- data %>% arrange(tracking)
data <- data %>% filter(Seeds.mixedTriplet.mean < 2000)
data <- data %>% filter(Hits.Pixel.mean > 0) %>% filter(Hits.Strip.mean > 0)

# Create plots
data %>%
  filter(fill__era %in%  c("2018B", "2018D")) %>%
  ggplot(aes(Seeds.pixelLess.mean, Seeds.mixedTriplet.mean, colour=tracking)) +
  geom_point(alpha=0.5) +
  scale_color_brewer(palette="Dark2") +
  xlab("Mean number of pixelLess seeds ") +
  ylab("Mean number of mixedTriplet seeds ") +
  ggtitle("Number of seeds for the era 2018B and 2018D")
ggsave("images/seeds.png", width = 6, height=6)
ggsave("images/seeds.pdf", width = 6, height=6)

data %>%
  filter(fill__era %in%  c("2018B", "2018D")) %>%
  ggplot(aes(Seeds.pixelLess.mean, Seeds.mixedTriplet.mean, colour=tracking)) +
  geom_point() +
  xlab("Mean number of pixelLess seeds") +
  ylab("Mean number of mixedTriplet seeds") +
  ggtitle("Number of seeds for the era 2018B and 2018D") +
  # geom_smooth(alpha=0.5) +
  facet_grid(. ~ fill__era) +
  scale_color_brewer(palette="Dark2")
ggsave("images/seeds_per_era.png", width = 6, height=6)
ggsave("images/seeds_per_era.pdf", width = 6, height=6)
