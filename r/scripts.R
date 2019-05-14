factorify <- function(data){
    data$pixel <- factor(data$pixel, levels=c("GOOD", "BAD", "EXCLUDED", "STANDBY"))
    data$strip <- factor(data$strip, levels=c("GOOD", "BAD", "EXCLUDED", "STANDBY"))
    data$tracking <- factor(data$tracking, levels=c("GOOD", "BAD", "EXCLUDED", "STANDBY"))
    data$reco <- factor(data$reco, levels=c("online", "express", "prompt", "rereco"))
    return(data)
}

# Histogram.Measure, Value, pixel, strip, tracking
tidify_1 <- function(data, remove_missing_values=TRUE){
    data <- data %>% gather(Histogram.Measure, Value, contains(".rms"), contains(".mean"), contains(".integral"), contains(".entries"))
    if(remove_missing_values){
        data %>% drop_na(Value)
    }
}

# Histogram, Measure, Value, pixel, strip, tracking
tidify_2 <- function(data){
    data %>%
        tidify_1 %>%
        mutate(Histogram.Measure = sub(".rms", ";rms", Histogram.Measure)) %>%
        mutate(Histogram.Measure = sub(".mean", ";mean", Histogram.Measure)) %>%
        mutate(Histogram.Measure = sub(".entries", ";entries", Histogram.Measure)) %>%
        mutate(Histogram.Measure = sub(".integral", ";integral", Histogram.Measure))  %>%
        separate(Histogram.Measure, c("Histogram", "Measure"), sep=";")
}

# Histogram, Measure, Value, Subcomponent, Status
tidify_3 <- function(data){
    data %>%
        tidify_2 %>%
        gather(Subcomponent, Status, pixel, strip, tracking)
}

# Histogram, rms, mean, entries, integral, pixel, strip, tracking
widify_1 <- function(data){
    data %>%
        tidify_2 %>%
        spread(Measure, Value)
}

# Histogram, rms, mean, entries, integral, Subcomponent, Status
widify_2 <- function(data){
    data %>%
        widify_1 %>%
        gather(Subcomponent, Status, pixel, strip, tracking)
}


# Histogram, rms, mean, entries, integral, pixel, strip, tracking
widify_3 <- function(data){
    data %>%
        widify_1 %>%
        unite(era_reco, fill__era, reco, sep=", ")
}


scale_this <- function(x){
    (x - mean(x, na.rm=TRUE)) / sd(x, na.rm=TRUE)
}

scale_features <- function(data, begin_index, end_index){
    data %>% mutate_at(c(begin_index:end_index), scale_this)
}

scale_histograms <- function(data){
    first_index <- grep("Chi2oNDF.rms", colnames(data))
    last_index <- grep("clusters.OffTrack.TEC.PLUS.integral", colnames(data))
    data %>% scale_features(first_index, last_index)
}

exclude_zero_hits <- function(data){
    data %>%
        filter(Hits.Pixel.rms > 0) %>%
        filter(Hits.Strip.rms > 0)
}
