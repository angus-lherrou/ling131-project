'''This script counts the dispersion of the points in a station's data.
Furthermore, it counts the approximate number of locations per 1000 tokens
for a station."

import os
import json
import numpy
import math

def getstationdispersion(station):
    if os.path.isdir("data/" + station):
        shows = os.listdir("data/" + station)
        lats = []
        longs = []
        assigned = False
        tokens = 0
        location_number = 0
        for show in shows:
            if os.path.isdir("data/" + station +"/"+ show):
                jsons = os.listdir("data/" + station +"/"+ show)
                for j in jsons:
                    with open("data/"+ station + "/" + show + "/" + j, 'rb') as f:
                        episodes = json.load(f)
                    for episode in episodes:
                        station_loc = episode['city'] + ", " + episode['state']             
                        locs = episode['locations']
                        location_number = len(locs) + location_number
                        oneline = episode['content'].replace("\n", " ")
                        tokens = len(oneline.split(" ")) + tokens
                        assigned = True
                        for entry in locs:
                            if entry[1] != None and entry[2] != None:
                                lats.append(entry[1])
                                longs.append(entry[2])
        if assigned:
            sigmalat = numpy.std(lats)
            sigmalong = numpy.std(longs)
            return (round(sigmalat * sigmalong * math.pi), station, station_loc, location_number/tokens)
        return None

stations = os.listdir("data")
dispersions = []
for station in stations:
    if os.path.isdir("data/" + station):
        dispersion = getstationdispersion(station)
        if dispersion != None:
            dispersions.append(getstationdispersion(station))
dispersions.sort()
for x in dispersions:
    print(x[1] + ", " + x[2] +  ": " + str(int(x[0])) + ", locations per 1000 tokens: " + str(round(x[3]*1000)))
