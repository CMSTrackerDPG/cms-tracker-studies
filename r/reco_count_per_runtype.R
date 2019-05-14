library(tidyverse)

# Read the data
data <- read_csv("data/data.csv")

# Manipulate data
data$fill__era <- factor(data$fill__era, levels=c("Commissioning2018", "2018A", "2018B", "2018C", "2018D", "2018E", "HIRun2018", "HIRun2018A"))
data$tracking <- factor(data$tracking, levels=c("GOOD", "BAD"))
data <- data %>% arrange(tracking)

# Create a plot
ggplot(data, aes(reco, fill=tracking)) +
    geom_bar() +
    scale_fill_brewer(palette="Dark2") +
    facet_grid(. ~ runtype)

# Save plot as file
ggsave("images/reco_count_per_runtype.png", width = 10, height=5)
