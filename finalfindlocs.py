import re
import pickle
import json
import geocoder
import os
import spacy
import pandas as pd 
nlp = spacy.load("en_core_web_sm")


STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida',
          'Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland',
          'Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire',
          'New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon',
          'Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia',
          'Washington','West Virginia','Wisconsin','Wyoming','District of Columbia']


''' Get dictionary of found coordinates''''
def get_geonames_dict(path):
    if os.path.exists(path):
        with open(path) as in_data:
            return pickle.load(in_data)
    return {}


'''Update found coordinate dictionary'''
def update_dict(geonames_dict, loc, gn_obj):
    geonames_dict[loc] = {}
    geonames_dict[loc]['state'] = gn_obj.state
    geonames_dict[loc]['country'] = gn_obj.country
    geonames_dict[loc]['coords'] = gn_obg.latlng
    return geonames_dict


'''Catches over limit error from geocoder'''
def catch_exceed_error(gn_obj):
    try:
        if gn_obj.value == 19:
            return 1
    except AttributeError:
        return None
   

'''Identify place names in Named Entities'''          
def find_locs(string):
    doc = nlp(string)
    duos = [X.text for X in doc.ents if X.label_ == 'GPE']
    return duos 


'''Determine if city is in station state'''
def city_in_state(geonames_data, li):
    i = 1
    while i < len(li):
        if li[i] in STATES:
            prev_loc_name = li[i - 1]
            if prev_loc_name in geonames_data.keys():
                loc_state = geonames_data[prev_loc_name]['state']
            else:
                loc = geocoder.geonames(prev_loc_name, key='krajovic')
                geonames_data = update_dict(geonames_data, prev_loc_name, loc)
                loc_state = geonames_data[prev_loc_name]['state']
            if li[i] == loc_state and (li[i] != li[i-1] or li[i-1] == 'New York'):
                li[i-1] = li[i-1] + ' ' + li[i]
                li.pop(i)                      #
                i -= 1
        i += 1
    return geonames_data


'''not_found array stores locations with no GPS data to reduce queries'''
def get_not_found_locs(path):
    if os.path.exists(path):
        with open(path) as in_data:
            return pickle.load(in_data)
    return []


'''Find coordinates for locations in a list of identifies place names.
Inputs: geonames dictionary, list of place names. '''
def find_coords(geonames_data, loc_list):
    coord_list = []
    not_found = get_not_found_locs('notfound.pkl')
    for loc in loc_list:
        if loc in geonames_data.keys(): 
            geo_loc = geonames_data[loc]
            latlong = geo_loc['coords']
            if latlong:
                geo_info = (loc, float(latlong[0]), float(latlong[1]))
                coord_list.append(geo_info)
                continue
            not_found.append(loc.lower())                
        else:
            if loc.lower() in not_found:
                continue
            geo_loc = geocoder.geonames(loc, key='krajovic')
            #check for exceed limit error
            if catch_exceed_error(geo_loc):
                return 0
            if geo_loc.latlng:
                geonames_data = update_dict(geonames_data, loc, geo_loc)
                latlong = geonames_data[loc]['coords']
                geo_info = (loc, float(latlong[0]), float(latlong[1]))
                coord_list.append(geo_info)
            else:
                not_found.append(loc.lower())
    return geonames_data, coord_list, not_found


'''Determine if location is in station state'''
def in_state(geonames_data, loc_list, ep):
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


'''Read in the json array for the show'''
def get_json_array(path):
    if os.path.exists(path):
         with open(jsonpath, 'r') as f:
            json_arr = json.load(f)
    else:
        json_arr = []
    return json_arr


'''Get location data'''
def get_data(infile, outpath):
    geonames_data = get_geonames_dict('geonamesobj.pkl')

    with open(infile,'r') as infile:
        episode = json.load(infile)

    ep_text = episode['content']
    ep_loc_list = find_locs(ep_text)
    geonames_data = city_in_state(geonames_data, ep_loc_list)
    
    geonames_data, loc_coords, not_found = find_coords(geonames_data, ep_loc_list)
    if loc_coords == None:
        return 0
    
    episode['locations'] = loc_coords
    episode['not_found'] = not_found
    
    ep_loc = episode['city'] + ', ' + episode['state']

    if ep_loc not in geonames_data.keys():
        ep_geo = geocoder.geonames(ep_loc, key='krajovic')
        if catch_exceed_error(ep_geo):
            return 0
        geonames_data = update_dict(geonames_data, ep_loc, ep_geo)

    ep_lat = float(geonames_data[ep_loc]['coords'][0])
    ep_long = float(geonames_data[ep_loc]['coords'][1])

    episode['ep_coords']= (ep_loc, ep_lat, ep_long)

    in_c, out_c, in_s, out_s = in_state(geonames_data, loc_coords, episode)
    
    episode['in_country'] = in_c
    episode['out_country'] = out_c
    episode['in_state'] = in_s
    episode['out_state'] = out_s
    
    with open('geonamesobjs.pkl', 'wb') as geo_dict:
        pickle.dump(geonames_data, geo_dict)
    
    #concatenate to show json array
    outfile = os.path.split(outpath)[1] + '.json'
    jsonpath = os.path.join(outpath, outfile)
    arr = get_json_arr(jsonpath)
    arr.append(episode)
    
    with open(jsonpath, 'w') as f:
        json.dump(arr, f)
    return 1
