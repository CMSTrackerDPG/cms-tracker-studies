# ml-tracker

Machine learning for CMS tracker data certification


## Requirements

- Python 3.6

## Prerequisites


To retrieve all data from the [CMS GUI](https://cmsweb.cern.ch/dqm/offline/) and [Run Registry](https://cmswbmoffshift.web.cern.ch/cmswbmoffshift/runregistry_offline/index.jsf) you have to install [runregcrawlr](https://github.com/ptrstn/runregcrawlr) and [dqmcrawlr](https://github.com/ptrstn/dqmcrawlr):

```bash
pip install git+https://github.com/ptrstn/dqmcrawlr
pip install git+https://github.com/ptrstn/runregcrawlr
```

### Retrieve Tracking maps

After installing ```dqmcrawlr``` and ```runregcrawlr```, you can generate a ```runs.txt``` file

```bash
runregcrawl --runs-txt --min 313052 --max 327564
```

This file can be used as input for ```dqmcrawlr```:

```bash
dqmcrawl runs.txt --trackingmap
```

After running that command a new folder ```TrackEtaPhi_ImpactPoint_GenTk```, containing 2869 json files,  should exist.

### Retrieve data

```bash
runregcrawl --min 313052 --max 327564
runregcrawl --tracker-lumis --min 313052 --max 327564
```
