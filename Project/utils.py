import pandas as pd
import altair as alt
from datetime import datetime
from altair import datum
import geopandas as gpd
import requests
import json

def create_nominatim_request(region_or_city):
    place_words = region_or_city.split(' ')
    request = "https://nominatim.openstreetmap.org/search.php?q="
    for word in place_words:
        request += f"+{word}"
    request += "+&format=jsonv2"
    
    # print(request)
    
    return request

def get_osm_id(region_or_city):
    request = create_nominatim_request(region_or_city)
    response = requests.get(request)
    
    # print(response.json())
    
    if region_or_city.lower() == 'коломийський район':
        print("using old коломийський")
        return 1741643
    # elif region_or_city.lower() == 'НАДВІРНЯНСЬКИЙ РАЙОН'.lower():
    #     return 1741645
    
    return response.json()[0]['osm_id']

def get_lat_lon(region_or_city):
    request = create_nominatim_request(region_or_city)
    response = requests.get(request)
    
    return (float(response.json()[0]['lat']), float(response.json()[0]['lon']))

def get_polygon_df_by_osm_id(osm_id):
    request = f"http://polygons.openstreetmap.fr/get_geojson.py?id={osm_id}&params=0"
    
    # print(request)

    return gpd.read_file(f"http://polygons.openstreetmap.fr/get_geojson.py?id={str(osm_id)}&params=0")

def get_region_geodata(region_or_city):
    osm_id = get_osm_id(region_or_city)
    
    return get_polygon_df_by_osm_id(osm_id)

def get_region_geometry(region_or_city):
    osm_id = get_osm_id(region_or_city)
    request = f"http://polygons.openstreetmap.fr/get_geojson.py?id={osm_id}&params=0"
    response = requests.get(request)
    
def visualize_place(region_or_city):
    df = get_region_geodata(region_or_city)
    
    lat, lon = get_lat_lon(region_or_city)

    return alt.Chart(df).mark_geoshape(stroke = 'white', strokeWidth = 2).encode(
        color = alt.value('gray'),
        opacity = alt.value(0.6),
    ).project(
        type='mercator', scale=12000, center=[lon, lat]
    ).properties(width = 550, height = 720)