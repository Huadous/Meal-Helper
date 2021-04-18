import requests
import sqlite3
import json
import restaurant
import plotly
import plotly.graph_objs as go
import database
import cache

import pandas as pd
import numpy as np

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from secrets import API_KEY


yelp_fusion_business_search_url = 'https://api.yelp.com/v3/businesses/search'
headers = {"Authorization": "Bearer {}".format(API_KEY)}

def api_search(category, location, offset=0):
    file_name = category + '_' + location + '_' + str(offset)
    file_type = 'restaurant_search'
    api_search = cache.sync_cache(file_name, file_type)
    if api_search == {}:
        params = {
            'categories' : category, 
            'location' : location, 
            'offset' : offset,
            'limit' : 50
            }
        r = requests.get(yelp_fusion_business_search_url, headers=headers, params=params)
        api_search = json.loads(r.text)
        cache.save_cache(file_name, file_type, api_search)
    return api_search

def api_search_all_data(category, location, db):
    LIMIT = 50
    cur = 0
    init_search = api_search(category, location, offset=cur)
    if 'error' in init_search:
        return []
    if init_search['total'] < LIMIT:
        LIMIT = init_search['total']
    data_collection = init_search['businesses']
    cur += 50
    while cur < LIMIT:
        data_collection.extend(api_search(category, location, offset=cur)['businesses'])
        cur += 50
        
    db.insert_restaurant_info(data_collection, category, location)
    return data_collection

def create_average_rating(category, city, db):
    print(db.get_average_rating_by_category_and_city(category, city))
    return db.get_average_rating_by_category_and_city(category, city)[0]

def create_average_rating_graph(city, db):
    restaurant_category_all = db.get_restaurant_category_all()
    average_rating = []
    for category in restaurant_category_all:
        api_search_all_data(category, city, db)
        average_rating.append(create_average_rating(category, city, db))
    print(restaurant_category_all)
    print(average_rating)
    xvals = []
    yvals = []
    for i in range(len(restaurant_category_all)):
        if average_rating[i] != None:
            yvals.append(average_rating[i])
            xvals.append(restaurant_category_all[i])
    yvals, xvals = zip(*sorted(zip(yvals, xvals),reverse=True))
    print(yvals)
    print(xvals)
    bar_data = [go.Bar(x=xvals, y=yvals)]
    return json.dumps(bar_data, cls=plotly.utils.PlotlyJSONEncoder)
    

