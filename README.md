[![Build Status](https://travis-ci.com/CMSTrackerDPG/cms-tracker-studies.svg?branch=master)](https://travis-ci.com/CMSTrackerDPG/cms-tracker-studies)

# CMS Tracker Studies

## Requirements

- Python 3.6

## Installation

```bash
git clone https://github.com/CMSTrackerDPG/cms-tracker-studies
cd cms-tracker-studies
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Get Data

You **need data** before you can create any plots. All data has to be put into the *data* directory.

```bash
mkdir -p data
```

Then either copy existing data in to the data folder or retrieve all the data from scratch. To retreive data from scratch check out [cms-tracker-studies-notebook](https://github.com/ptrstn/cms-tracker-studies-notebook).

## R plots

Example R plots are available in the ```r-plots``` folder.

First you have to export you data in a csv format

```bash
python examples/export_to_csv.py 
```

Make sure you have created a folder for you plot images:

```bash
mkdir -p images
```

Install all necessary R libraries (if not done already):

```bash
R
```

```r
install.packages("tidyverse")
install.packages("corrr")
install.packages("corrplot")
install.packages("GGally")
q()
Save workspace image? [y/n/c]: n
```

Then you can run the R scripts:

```bash
R -f r/seeds.R
R -f r/hits.R
R -f r/correlation_matrix.R
```

All images will be stored in the ```images``` folder.

## Dokumentation

Check out the [cms-tracker-studies-notebook](https://github.com/ptrstn/cms-tracker-studies-notebook)
