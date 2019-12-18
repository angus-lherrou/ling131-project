"""radiomap.py

Script to generate heatmap images given a JSON file.

Author: Angus L'Herrou

Broken with current PIP repo. To run, install with conda in a fresh VENV:

conda config --add channels conda-forge
conda config --set channel_priority strict
conda install -y -c conda-forge libgdal
conda install -y -c conda-forge gdal
conda install -y -c conda-forge proj
conda install -y -c conda-forge cartopy
conda install -y -c conda-forge geoplot
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
import pickle

logging.captureWarnings(True)


def get_data(path, datatype='dataframe'):
    if datatype == 'json':
        with open(path, 'r') as jsn:
            stations = json.load(jsn)
        station_list = list(stations.items())
        df_precursor = {'name': [name for name, xy in station_list],
                        'longitude': [y for name, [x, y] in station_list],
                        'latitude': [x for name, [x, y] in station_list]}
        stations_df = pd.DataFrame.from_dict(df_precursor)
    elif datatype == 'pickle':
        with open(path, 'rb') as pkl:
            stations = pickle.load(pkl)
        station_list = [tpl for tpl in stations if type(tpl) == tuple]
        df_precursor = {'name': [name for name, lat, long in station_list],
                        'longitude': [long for name, lat, long in station_list],
                        'latitude': [lat for name, lat, long in station_list]}
        stations_df = pd.DataFrame.from_dict(df_precursor)
    elif datatype == 'dataframe':
        stations_df = pd.read_pickle(path)
    else:
        raise Exception('Not a valid data type!')
    return stations_df


def get_gdf(data, crs=4326):
    """
    Method to get the locations of all stations in the 'locations' file and store
    them in a GeoDataFrame as Points.
    :param data: a DataFrame with columns 'title', 'longitude', 'latitude'
    :param crs: the EPSG projection to use
    :return: a GeoDataFrame with columns 'title' and 'geometry'.
    """
    geometry = [Point(xy) for xy in zip(data['longitude'], data['latitude'])]
    data = data.drop('longitude', axis=1).drop('latitude', axis=1)
    return gpd.geodataframe.GeoDataFrame(data,
                                         crs={'init': 'epsg:4326'},
                                         geometry=geometry,
                                         ).to_crs(epsg=crs)


def get_single_point(lat_long, crs=4326):
    data = pd.DataFrame.from_dict({'title': ['origin'],
                                   'geometry': [Point((lat_long[1], lat_long[0]))]})
    return gpd.geodataframe.GeoDataFrame(data,
                                         crs={'init': 'epsg:4326'},
                                         ).to_crs(epsg=crs)


def gen_map(path, datatype='dataframe', figsize=(16, 12), levels=25):
    """
    Generates a png file at maps/{name}.png with a heatmap of points in the JSON file at {path},
    projected onto the contiguous US using Albers Equal Area Projection.
    :param levels: the number of isolines to generate the heatmap with
    :param datatype: how the data at 'path' is formatted. Leave as 'dataframe'.
    :param name: the name of the file before the .png extension
    :param path: the path where the JSON file is located
    :param figsize: the pyplot figure size of the plot. This determines the final resolution.
    :return: None; writes an image file to disk
    """
    if not os.path.exists('maps'):
        os.mkdir('maps')

    contig = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
    us_extent = (-125, 25, -66, 48)

    points_df: pd.DataFrame = get_data(path, datatype)
    title = points_df.title.location
    origin = (points_df.latitude.location, points_df.longitude.location)
    points_df = points_df.drop('location')
    heatmap_points = get_gdf(points_df, crs=4326)

    poly = gplt.polyplot(contig,
                         projection=gcrs.AlbersEqualArea(central_longitude=-98,
                                                         central_latitude=39.5),
                         figsize=figsize,
                         extent=us_extent,
                         zorder=1)

    heatmap = gplt.kdeplot(heatmap_points,
                           clip=contig.geometry,
                           shade=True,
                           cmap='Purples',
                           extent=us_extent,
                           n_levels=levels,
                           ax=poly, zorder=0)

    '''Strip points of duplicates for efficiency when drawing points'''

    to_drop = []
    places = set()

    for row in points_df.iterrows():
        place = row[1].title
        if place in places:
            to_drop.append(row[0])
        places.add(place)

    for item in to_drop:
        points_df = points_df.drop(item)

    points = get_gdf(points_df, crs=4326)

    gplt.pointplot(points, ax=poly, s=1, color='k',
                   extent=us_extent, zorder=2)

    origin_gdf = get_single_point(origin)
    gplt.pointplot(origin_gdf, ax=poly, marker='*', s=5,
                   color='#ff7f0e', extent=us_extent, zorder=4)

    plt.title(f'Location mentions for {title}: Contiguous U.S.')
    plt.savefig(f'maps/{title}.svg')

    # canvas = plt.get_current_fig_manager().canvas
    # canvas.draw()
    # size = canvas.get_width_height()
    # pil_image = Image.frombytes('RGB', size,
    #                             canvas.tostring_rgb())
    # crop_coords = (int(500*figsize[0]/32), int(440*figsize[1]/24),
    #                int(2640*figsize[0]/32), int(1920*figsize[1]/24))
    # pil_image = pil_image.crop(crop_coords)
    # pil_image.save(f'maps/{name}.png')
