import re
import pickle
import json
import geocoder
import os
import spacy
import pandas as pd 
#import en_core_web_sm
nlp = spacy.load("en_core_web_sm")


STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida',
          'Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland',
          'Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire',
          'New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon',
          'Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia',
          'Washington','West Virginia','Wisconsin','Wyoming','District of Columbia']



if os.path.exists('geonamesobjs.pkl'):
    with open('geonamesobjs.pkl','rb') as in_data:
        geonames_data = pickle.load(in_data)


else:
    geonames_data = {}


def find_locs(string):
    doc = nlp(string)
    duos = [X.text for X in doc.ents if X.label_ == 'GPE']
    return duos 


def city_in_state(li):
    i = 1
    while i < len(li):
        if li[i] in STATES:
            prev_loc_name = li[i - 1]
            if prev_loc_name in geonames_data.keys():
                loc_state = geonames_data[prev_loc_name]['state']
            else:
                loc = geocoder.geonames(prev_loc_name, key='krajovic')
                geonames_data[prev_loc_name] = {}
                geonames_data[prev_loc_name]['state'] = loc.state
                geonames_data[prev_loc_name]['country'] = loc.country
                geonames_data[prev_loc_name]['coords'] = loc.latlng
                loc_state = geonames_data[prev_loc_name]['state']

            if li[i] == loc_state and (li[i] != li[i-1] or li[i-1] == 'New York'):
                li[i-1] = li[i-1] + ' ' + li[i]
                li.pop(i)
                i -= 1
        i += 1


def find_coords(loc_list):
    coord_list = []
    not_found = []
    for loc in loc_list:
        if loc in geonames_data.keys():
            geo_loc = geonames_data[loc]
            latlong = geo_loc['coords']
            if latlong:
                geo_info = (loc, float(latlong[0]), float(latlong[1]))
                coord_list.append(geo_info)
            else:
                not_found.append(loc)
        else:
            geo_loc = geocoder.geonames(loc, key='krajovic')
            if geo_loc.latlng:
                geonames_data[loc] = {}
                geonames_data[loc]['state'] = geo_loc.state
                geonames_data[loc]['country'] = geo_loc.country
                geonames_data[loc]['coords'] = geo_loc.latlng

                latlong = geonames_data[loc]['coords']
                geo_info = (loc, float(latlong[0]), float(latlong[1]))
                coord_list.append(geo_info)
            else:
                not_found.append(loc)
    return coord_list, not_found


def create_df(coord_list, ep):
    ep_sta = ep['station']
    ep_loc = ep['ep_coords']

    ep_lat = float(ep['ep_coords'][1])
    ep_long = float(ep['ep_coords'][2])

    loc_df = {'location': [ep_sta, ep_lat, ep_long]}

    for i in range(len(coord_list)):
        loc = coord_list[i]
        if type(loc) == tuple:
            loc_df[str(i)] = [loc[0],loc[1],loc[2]]

    dataframe = pd.DataFrame.from_dict(loc_df,
                    orient='index',
                    columns=['title', 'latitude', 'longitude'])

    return dataframe

def in_state(loc_list, ep):
    ep_loc = ep['city'] + ', ' + ep['state']
    ep_state = geonames_data[ep_loc]['state']
    in_country = []
    out_country = []
    in_state = []
    out_state = []
    for location in loc_list:
            loc = location[0]
            geo_loc = geonames_data[loc]
            state = geo_loc['state']
            country = geo_loc['country']
            if state == ep_state:
                in_state.append(loc)
            else:
                out_state.append(loc)
            if country == 'United States':
                in_country.append(loc)
            else:
                out_country.append(loc)
    return in_country, out_country, in_state, out_state
    

def get_data(infile, outpath):
    with open(infile,'r') as infile:
        episode = json.load(infile)

    ep_text = episode['content']
    ep_loc_list = find_locs(ep_text)
    city_in_state(ep_loc_list)
    
    loc_coords, not_found = find_coords(ep_loc_list)
    
    episode['locations'] = loc_coords
    episode['not_found'] = not_found
    
    ep_loc = episode['city'] + ', ' + episode['state']

    if ep_loc not in geonames_data.keys():
        ep_geo = geocoder.geonames(ep_loc, key='krajovic')
        try:
            if ep_geo.value == 19:
                return 0
        except AttributeError:
            None
        geonames_data[ep_loc] = {}
        geonames_data[ep_loc]['state'] = ep_geo.state
        geonames_data[ep_loc]['country'] = ep_geo.country
        geonames_data[ep_loc]['coords'] = ep_geo.latlng

    ep_lat = float(geonames_data[ep_loc]['coords'][0])
    ep_long = float(geonames_data[ep_loc]['coords'][1])

    episode['ep_coords']= (ep_loc, ep_lat, ep_long)

    in_c, out_c, in_s, out_s = in_state(loc_coords,episode)
    
    episode['in_country'] = in_c
    episode['out_country'] = out_c
    episode['in_state'] = in_s
    episode['out_state'] = out_s
    
    with open('geonamesobjs.pkl', 'ab') as geo_dict:
        pickle.dump(geonames_data, geo_dict)
    
    outfile = os.path.split(outpath)[1] + '.json'
    jsonpath = os.path.join(outpath, outfile)
    
    if os.path.exists(jsonpath):
         with open(jsonpath, 'r') as f:
            arr = json.load(f)
    else:
        arr = []
    arr.append(episode)
    with open(jsonpath, 'w') as f:
        json.dump(arr, f)
    return 1
