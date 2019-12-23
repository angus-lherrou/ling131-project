# ling131-project
final project by angus, dom, james, katie, and miriam

#### Overview

This project examines a corpus of transcribed radio data for trends in mentioned locations relative to the location of the radio station. The corpus is built using the RadioTalk corpus, `spacy`, and `geonames`.

#### Running the main script

To run our main script, set up a clean Conda Python 3.7 interpreter and run the following:

```
  $ conda config --add channels conda-forge
  $ conda config --set channel_priority strict
  $ conda install -y -c conda-forge geoplot
  $ python main.py
```

#### Required Packages

Our main script requires the following packages to run:
* `geopandas`
* `geoplot`
* `json`
* `logging`
* `matplotlib`
* `os`
* `pandas`
* `shapely`


#### Project Presentation  
https://docs.google.com/presentation/d/1GB_f5kugE6EfKw064cTWvjeSPfuPjTaVbMl1ayRMAWs/edit#slide=id.g6c2b65194f_1_13

#### Spacy Named Entity Recognition Resource  
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da

#### Map generation tutorial  
[MAPS.md](MAPS.md)
