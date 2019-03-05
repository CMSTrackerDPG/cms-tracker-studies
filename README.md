[![Build Status](https://travis-ci.com/ptrstn/cms-tracker-studies.svg?branch=master)](https://travis-ci.com/ptrstn/cms-tracker-studies)

# CMS Tracker Studies

## Requirements

- Python 3.6

## Installation

```bash
pip install git+https://github.com/ptrstn/cms-tracker-studies
```

## Prerequisites

To retrieve the necessary data you have to install the following tools:

```bash
pip install git+https://github.com/ptrstn/dqmcrawlr
pip install git+https://github.com/ptrstn/runregcrawlr
pip install git+https://github.com/ptrstn/wbmcrawlr
pip install git+https://github.com/ptrstn/twikirefs
```


## Data Retrieval

```bash
wbmcrawl --runs 313052 327564
wbmcrawl --fills 6477 7492
```