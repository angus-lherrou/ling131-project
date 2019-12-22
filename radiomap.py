"""radiomap.py

Script to generate heatmap images given a pickled DataFrame.

Author: Angus L'Herrou

Broken with current PIP repo. To run, install with conda in a fresh VENV:

conda config --add channels conda-forge
conda config --set channel_priority strict
conda install -y -c conda-forge geoplot
"""


import os
import logging
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geoplot as gplt
from geoplot import crs as gcrs


logging.captureWarnings(True)


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
    """
    Method to create a GeoDataFrame for a single point for plotting one point with GeoPlot
    :param lat_long: a tuple
    :param crs: desired CRS for plotting
    :return: a GeoDataFrame containing one Point with the title 'origin'
    """
    data = pd.DataFrame.from_dict({'title': ['origin'],
                                   'geometry': [Point((lat_long[1], lat_long[0]))]})
    return gpd.geodataframe.GeoDataFrame(data,
                                         crs={'init': 'epsg:4326'},
                                         ).to_crs(epsg=crs)


def gen_map(path, figsize=(16, 12), levels=25, force=False):
    """
    Generates a png file at maps/{name}.png with a heatmap of points in the JSON file at {path},
    projected onto the contiguous US using Albers Equal Area Projection.
    :param path: the path where the JSON file is located
    :param figsize: the pyplot figure size of the plot. This determines the final resolution.
    :param levels: the number of isochrones to generate the heatmap with
    :param force: if True, generate map even if it already exists
    :return: the file path where the map is
    """
    if not os.path.exists('maps'):
        os.mkdir('maps')

    contiguous = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))
    us_extent = (-125, 25, -66, 48)

    points_df: pd.DataFrame = pd.read_pickle(path)
    title = points_df.title.location
    out_path = f'maps/{title}.png'

    if force or not os.path.exists(out_path):
        origin = (points_df.latitude.location, points_df.longitude.location)
        points_df = points_df.drop('location')

        poly = gplt.polyplot(contiguous,
                             projection=gcrs.AlbersEqualArea(central_longitude=-98,
                                                             central_latitude=39.5),
                             figsize=figsize,
                             extent=us_extent,
                             zorder=1)

        gplt.kdeplot(get_gdf(points_df, crs=4326),
                     clip=contiguous.geometry,
                     shade=True,
                     cmap='viridis',
                     shade_lowest=True,
                     extent=us_extent,
                     n_levels=levels,
                     ax=poly, zorder=0)

        """Deprecated: SVG optimizations"""
        # to_drop = []
        # places = set()
        #
        # for row in points_df.iterrows():
        #     place = row[1].title
        #     if place in places:
        #         to_drop.append(row[0])
        #     places.add(place)
        #
        # for item in to_drop:
        #     points_df = points_df.drop(item)

        gplt.pointplot(get_gdf(points_df, crs=4326), ax=poly, s=1, color='k',
                       extent=us_extent, zorder=2)

        gplt.pointplot(get_single_point(origin), ax=poly, marker='*', s=5,
                       color='#ff7f0e', extent=us_extent, zorder=4)

        plt.title(f'Location mentions for {title}: Contiguous U.S.')
        plt.savefig(out_path)
        return out_path
