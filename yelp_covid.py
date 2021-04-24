import requests
import sqlite3
import json
import plotly
import plotly.graph_objs as go
import database
import cache
import folium
import time
import os


import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from folium import CustomIcon

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}

def make_path():
    if not os.path.exists(r'./maps'):
        os.makedirs(r'./maps')
    print("[YELP_COVID]->make_path:         [YES]-> './maps'")

def visit_by_url(url):
    print('[YELP_COVID]->visit_by_url:      [url]-> '+ make_name_readable(url))
    file_name = file_name_generator(url)
    file_type = 'covid_services'
    html_file = cache.sync_cache(file_name, file_type)
    if html_file == {} or len(html_file) == 0:
        print('[YELP_COVID]->visit_by_url:      [CRAWLING]-> '+ make_name_readable(url))
        r = requests.get(url, headers=headers)
        html_file = r.text
        cache.save_cache(file_name, file_type, html_file)
    return html_file

def make_name_readable(name):
    if len(name) > 50:
        return name[0:50] + '...'
    return name + '.json'

def file_name_generator(name_input):
    name = name_input.replace('/', '~')
    name = name.replace('\\', '@')
    name = name.replace('*', '#')
    name = name.replace('"', '$')
    name = name.replace('<', '%')
    name = name.replace('>', '^')
    name = name.replace('|', '(')
    name = name.replace('?', ')')
    return name

def get_covid_info(url):
    html = visit_by_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    service_part = soup.find_all('div', class_ = 'margin-t2__373c0__1CFWK')[0:2]
    dataset = []
    for i in range(2):
        dataset.append([])
        if i >= len(service_part):
            continue
        data = service_part[i].find_all('div', class_="margin-r3__373c0__r37sx")
        for ele in data:
            name = str(ele.find('span', class_ = "css-1h1j0y3").contents[0])
            status = bool(ele.find('path')['d'] == 'M9.46 17.52a1 1 0 01-.71-.29l-4-4a1.004 1.004 0 111.42-1.42l3.25 3.26 8.33-8.34a1.004 1.004 0 011.42 1.42l-9 9a1 1 0 01-.71.37z')
            dataset[i].append([name, status])
    print('[YELP_COVID]->get_covid_info:    [SCRAPING]-> '+ make_name_readable(url))
    return dataset
            
def make_info_readable(table_basic_info):
    covid_info = []
    for ele in table_basic_info:
        url = ele[1]
        dataset = get_covid_info(url)
        string_1 = ''
        string_2 = ''
        for ele in dataset[0]:
            if ele[1]:
                string_1 += str(ele[0]) + ' : ✔<br>'
            else:
                string_1 += str(ele[0]) + ' : ✖<br>'
        for ele in dataset[1]:
            if ele[1]:
                string_2 += str(ele[0]) + ' : ✔<br>'
            else:
                string_2 += str(ele[0]) + ' : ✖<br>'
        covid_info.append([string_1, string_2])
        print ("[YELP_COVID]->create_table_with_data_information:                   [{:3.0%}]".format(len(covid_info)/len(table_basic_info)))
    return covid_info

# def draw_custom_icon(m, restaurant_locations_data):
#     for data in restaurant_locations_data:
#         marker = folium.Marker(
#             location=[data[1], data[2]], 
#             popup=data[0],
#             icon=folium.Icon(color="red",icon="glyphicon glyphicon-cutlery")).add_to(m)
        # folium.Marker(
        # location=[25.0431, 121.539723], 
        # icon=folium.Icon(color="red",icon="fa-truck", prefix='fa')).add_to(m)
 
def get_map(city_location, restaurant_locations_data):
    
    df = pd.DataFrame(restaurant_locations_data, columns=['name', 'Lat', 'Long'])
    m = folium.Map(df[['Lat', 'Long']].mean().values.tolist(),  # 地图中心
                     tiles='OpenStreetMap')  # stamentoner,Stamen Watercolor,OpenStreetMap'

    for name, lat, lon in zip(df['name'], df['Lat'], df['Long']):
        folium.Marker(
            location=[lat, lon], 
            popup=name,
            icon=folium.Icon(color="red",icon="glyphicon glyphicon-cutlery")).add_to(m)

    sw = df[['Lat', 'Long']].min().values.tolist()
    ne = df[['Lat', 'Long']].max().values.tolist()
    # m.fit_bounds([sw, ne]) 
    time_stamp = time.time()
    m.save('maps/' + str(time_stamp) + '.html')
    print('[YELP_COVID]->get_map:           [MAP]-> '+ str(city_location))
    return time_stamp