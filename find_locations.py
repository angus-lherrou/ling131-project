import spacy
# from pprint import pprint
from spacy import displacy
import en_core_web_sm
from geopy.geocoders import Nominatim
import pickle
import nltk
from adapted_main_a4 import Text
from collections import Counter

geolocator = Nominatim()




try:
  duos = pickle.load(open("pickledLocLabelTuples", 'rb'))
except:
   print("failed to load pickled tuples")
   wbur1 = Text('WBUR_shownames')
   duos = wbur1.find_locs()
   with open("pickledLocLabelTuples", 'wb') as f:
     pickle.dump(duos, f)
print(duos)


all_locations = []
wrong = []
for item in duos:
    try:
      location = geolocator.geocode(item[0])
      lat_long = (location.latitude, location.longitude)
      all_locations.append(lat_long)
    except:
      wrong.append(item[0])
      print(item[0])
if len(all_locations) != 0:
    with open("pickledAllLocations", "wb") as f:
        pickle.dump(all_locations, f)
    print(all_locations[:10])
#try:
#  loc_counter = pickle.load(open("pickledLongLatCounter", 'rb'))
#except:
    loc_counter = Counter(all_locations)
    with open("pickledLongLatCounter", 'wb') as f:
      pickle.dump(loc_counter, f)

    print(loc_counter)
