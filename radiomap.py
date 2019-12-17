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


# def get_cities(crs=4326, states='all'):
#     path = 'data/cities.json'
#     cities_df = pd.read_json(path)
#     return get_points(cities_df, crs, states)
#
#
# def get_points(data, crs=4326, states='all'):
#     cities_df = data
#     if states == 'contiguous':
#         cities_df = cities_df[(cities_df.state != 'Alaska') & (cities_df.state != 'Hawaii')]
#     elif states == 'all':
#         pass
#     else:
#         cities_df = cities_df[cities_df.state == states]
#
#     geometry = [Point(xy) for xy in zip(cities_df['longitude'], cities_df['latitude'])]
#     return gpd.geodataframe.GeoDataFrame(cities_df,
#                                          crs={'init': 'epsg:4326'},
#                                          geometry=geometry
#                                          ).to_crs(epsg=crs)


def gen_map(name, path=LOCATIONS, figsize=(32, 24)):
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
    pil_image = pil_image.crop((640, 560, 2060, 1520))
    pil_image.save(f'maps/{name}.png')
