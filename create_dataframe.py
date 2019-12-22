import os
import json
import pickle
import pandas as pd


def make_show_df(direct):
    loc_df = {}
    all_locs = []

    with open(direct) as in_file:
        show_data = json.load(in_file)
    first_ep = show_data[0]
    ep_loc = first_ep['ep_coords']
    ep_lat = float(ep_loc[1])
    ep_long = float(ep_loc[2])
    loc_df['location'] = [first_ep['show_name'],ep_lat,ep_long]

    for episode in show_data:
        all_locs += episode['locations']

    for i in range(len(all_locs)):
        loc = all_locs[i]
        if type(loc) == list:
            loc_df[str(i)] = [loc[0],loc[1],loc[2]]

    df_for_map = pd.DataFrame.from_dict(loc_df, 
                    orient='index',
                    columns=['title', 'latitude', 'longitude'])

    return df_for_map


def make_station_df(direct):
    loc_df = {}
    all_locs = []

    show_list = [d for d in os.listdir(direct) if os.path.isdir(direct + '/' + d)]
    show_dir = [(direct + '/' + show + '/' + show + '.json') for show in show_list 
                           if os.path.isfile(direct + '/' + show + '/' + show + '.json')]

    with open(show_dir[0],'r') as in_file:
        first_file = json.load(in_file)
    first_ep = first_file[0]
    ep_loc = first_ep['ep_coords']
    ep_lat = float(ep_loc[1])
    ep_long = float(ep_loc[2])
    loc_df['location'] = [first_ep['station'],ep_lat,ep_long]

    for file in show_dir:
        with open(file, 'r') as in_file:
            show_data = json.load(in_file)
        for episode in show_data:
            all_locs += episode['locations']

    for i in range(len(all_locs)):
        loc = all_locs[i]
        if type(loc) == list:
            loc_df[str(i)] = [loc[0],loc[1],loc[2]]

    df_for_map = pd.DataFrame.from_dict(loc_df,
                    orient='index',
                    columns=['title', 'latitude', 'longitude'])

    return df_for_map
