"""radiomap.py

Script to generate heatmap images given a JSON file.

Author: Angus L'Herrou
"""

import geopandas as gpd
import os
import matplotlib.pyplot as plt
import logging
from shapely.geometry import Point
import pandas as pd
import geoplot as gplt
from geoplot import crs as gcrs
import json
from PIL import Image

logging.captureWarnings(True)

LOCATIONS = 'data/name_lat_long.json'


def get_stations(crs=4326, locations=LOCATIONS):
    """
    Method to get the locations of all stations in the 'locations' file and store
    them in a GeoDataFrame as Points.
    :param crs: the EPSG projection to use
    :param locations: the path to a JSON file with "'{name}': [{latitude}, {longitude}]" items
    :return: a GeoDataFrame with columns 'name', 'longitude', 'latitude', 'geometry'.
    """
    with open(locations, 'r') as jsn:
        stations: dict = json.load(jsn)
    station_list = list(stations.items())
    df_precursor = {'name': [name for name, xy in station_list],
                    'longitude': [y for name, [x, y] in station_list],
                    'latitude': [x for name, [x, y] in station_list]}
    stations_df = pd.DataFrame.from_dict(df_precursor)

    geometry = [Point(xy) for xy in zip(stations_df['longitude'], stations_df['latitude'])]
    return gpd.geodataframe.GeoDataFrame(stations_df,
                                         crs={'init': 'epsg:4326'},
                                         geometry=geometry
                                         ).to_crs(epsg=crs)


def gen_map(name, path=LOCATIONS, figsize=(32, 24)):
    """
    Generates a png file at maps/{name}.png with a heatmap of points in the JSON file at {path},
    projected onto the contiguous US using Albers Equal Area Projection.
    :param name: the name of the file before the .png extension
    :param path: the path where the JSON file is located
    :param figsize: the pyplot figure size of the plot. This determines the final resolution.
    :return: None; writes an image file to disk
    """
    if not os.path.exists('maps'):
        os.mkdir('maps')

    contig = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
    contig_cities = get_stations(4326, path)

    poly = gplt.polyplot(contig,
                         projection=gcrs.AlbersEqualArea(central_longitude=-98,
                                                         central_latitude=39.5),
                         figsize=figsize,
                         extent=(-125, 25, -66, 48),
                         zorder=1)

    cities_plot = gplt.kdeplot(contig_cities,
                               clip=contig.geometry,
                               shade=True,
                               cmap='Reds',
                               ax=poly)

    gplt.pointplot(contig_cities, ax=cities_plot, hue=[50]*107, cmap='gist_gray')
    plt.tight_layout()

    canvas = plt.get_current_fig_manager().canvas
    canvas.draw()
    size = canvas.get_width_height()
    pil_image = Image.frombytes('RGB', size,
                                canvas.tostring_rgb())
    crop_coords = (int(640*figsize[0]/32), int(560*figsize[1]/24),
                   int(2060*figsize[0]/32), int(1520*figsize[1]/24))
    pil_image = pil_image.crop(crop_coords)
    pil_image.save(f'maps/{name}.png')
