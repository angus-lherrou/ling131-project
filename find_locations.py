import spacy
# from pprint import pprint
from spacy import displacy
#from collections import Counter
import en_core_web_sm
from geopy.geocoders import Nominatim

import nltk
from main_a4 import Text 
from nltk import FreqDist

geolocator = Nominatim()


wbur1 = Text('WBUR_shownames')


duos = wbur.find_locs()
print(duos)

all_locations = []
wrong = []
for item in duos:
  try:
    location = geolocator.geocode(item[0])
    lat_long = (location.latitude, location.longitude)
    all_locations.append(lat_long)
  except:
    wrong.append(item)
  
loc_fdist = FreqDist(all_locations)


print(loc_fdist)