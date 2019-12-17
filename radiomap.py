import geopandas as gpd
import os
import matplotlib.pyplot as plt
import logging
from shapely.geometry import Point, Polygon
import pandas as pd
import geoplot as gplt
from geoplot import crs as gcrs
import json

logging.captureWarnings(True)

LOCATIONS = 'data/name_lat_long.json'


def get_stations(crs=4326, states='all'):
    with open(LOCATIONS, 'r') as jsn:
        stations: dict = json.load(jsn)
    station_list = list(stations.items())
    df_precursor = {'name': [name for name, xy in station_list],
                    'longitude': [y for name, [x, y] in station_list],
                    'latitude': [x for name, [x, y] in station_list]}
    stations_df = pd.DataFrame.from_dict(df_precursor)

    geometry = [Point(xy) for xy in zip(stations_df['longitude'], stations_df['latitude'])]
    return gpd.geodataframe.GeoDataFrame(stations_df, crs={'init': 'epsg:4326'}, geometry=geometry).to_crs(epsg=crs)


def get_cities(crs=4326, states='all'):
    path = 'data/cities.json'
    cities_df = pd.read_json(path)
    return get_points(cities_df, crs, states)


def get_points(data, crs=4326, states='all'):
    cities_df = data
    if states == 'contiguous':
        cities_df = cities_df[(cities_df.state != 'Alaska') & (cities_df.state != 'Hawaii')]
    elif states == 'all':
        pass
    else:
        cities_df = cities_df[cities_df.state == states]

    geometry = [Point(xy) for xy in zip(cities_df['longitude'], cities_df['latitude'])]
    return gpd.geodataframe.GeoDataFrame(cities_df, crs={'init': 'epsg:4326'}, geometry=geometry).to_crs(epsg=crs)


if __name__ == "__main__":
    # usa = gpd.read_file('./ne/ne_states/ne_50m_admin_1_states_provinces.shp')
    # contig = usa.tail(50)[usa.name_en != 'Hawaii']
    #
    # contig = contig.to_crs(epsg=2163)
    #
    # contig_cities = get_cities(2163, 'contiguous')
    #
    # usa_plot = contig.plot()
    # contig_cities.plot(ax=usa_plot, marker='.', color='red', markersize=5)
    # plt.axis('off')
    # plt.title('Radio Stations')
    # plt.savefig('graph.svg')

    if not os.path.exists('maps'):
        os.mkdir('maps')

    contig = gpd.read_file(gplt.datasets.get_path('contiguous_usa'))

    contig_cities = get_stations(4326, 'contiguous')

    cities_plot = gplt.kdeplot(contig_cities,
                               clip=contig.geometry,
                               shade=True, cmap='Reds',
                               projection=gcrs.AlbersEqualArea(), figsize=(16, 12))

    poly = gplt.polyplot(contig, ax=cities_plot, zorder=1)

    gplt.pointplot(contig_cities, ax=cities_plot, hue=[50 for x in range(107)], cmap='gist_gray')
    plt.axis('off')
    plt.savefig('maps/points.svg')
