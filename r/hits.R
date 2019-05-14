library(tidyverse)
library(corrplot)
library(corrr)

# Load the data
data <- read_csv("data/data.csv")

# Manipulate the data
data$tracking <- factor(data$tracking, levels=c("GOOD", "BAD"))
data$reco <- factor(data$reco, levels=c("online", "express", 'prompt', 'rereco'))
data <- data %>% filter(runtype=='collisions')
data <- data %>% arrange(tracking)
data <- data %>% filter(Hits.Pixel.rms > 0) %>%  filter(Hits.Strip.rms > 4)

# Create dataset for the 'grey' background points in the plot
gray_data <- data
gray_data$fill__era = '2018A'

tmp_data <- data
tmp_data$fill__era = '2018B'

gray_data <- bind_rows(gray_data, tmp_data)

tmp_data <- data
tmp_data$fill__era = '2018C'

gray_data <- bind_rows(gray_data, tmp_data)

tmp_data <- data
tmp_data$fill__era = '2018D'

gray_data <- bind_rows(gray_data, tmp_data)

tmp_data <- data
tmp_data$fill__era = 'HIRun2018A'

gray_data <- bind_rows(gray_data, tmp_data)

# Plot the data
data %>%
  ggplot(aes(Hits.Pixel.rms, Hits.Strip.rms, color=fill__era)) +
  geom_point(data=gray_data, color='gray', alpha=0.3) +
  geom_point(alpha=0.7) +
  scale_color_brewer(palette="Dark2") +
  labs(colour = "Era") +
  xlab("RMS of the number of hits in the pixel detector") +
  ylab("RMS of the number of hits in the strip detector") +
  facet_grid(. ~ fill__era)
ggsave("images/hits_pixel_vs_strip_color_era_gray_bg.png", width = 8, height=4)
ggsave("images/hits_pixel_vs_strip_color_era_gray_bg.pdf", width = 8, height=4)

# Create dataset for the 'grey' background points in the plot
gray_data2 <- data
gray_data2$reco = 'online'

tmp_data <- data
tmp_data$reco = 'express'

gray_data2 <- bind_rows(gray_data2, tmp_data)

tmp_data <- data
tmp_data$reco = 'prompt'

gray_data2 <- bind_rows(gray_data2, tmp_data)

tmp_data <- data
tmp_data$reco = 'rereco'

gray_data2 <- bind_rows(gray_data2, tmp_data)

data$reco <- factor(data$reco, levels=c('online', 'express', 'prompt', 'rereco'))
gray_data2$reco <- factor(gray_data2$reco, levels=c('online', 'express', 'prompt', 'rereco'))

# Plot the data
data %>%
  ggplot(aes(Hits.Pixel.rms, Hits.Strip.rms, color=reco)) +
  geom_point(data=gray_data2, color='gray', alpha=0.3) +
  geom_point(alpha=0.7) +
  scale_color_brewer(palette="Dark2") +
  labs(colour = "Reconstruction") +
  xlab("RMS of the number of hits in the pixel detector") +
  ylab("RMS of the number of hits in the strip detector") +
  facet_grid(. ~ reco)

ggsave("images/hits_pixel_vs_strip_color_reco_gray_bg.png", width = 8, height=4)
ggsave("images/hits_pixel_vs_strip_color_reco_gray_bg.pdf", width = 8, height=4)
