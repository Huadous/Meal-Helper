import requests
import sqlite3
import json
import plotly
import plotly.graph_objs as go
import database
import cache
import yelp_fusion
import copy
import yelp_covid
import folium
import time

import pandas as pd
import numpy as np

from flask import Flask, render_template, request, send_file, url_for
from flask_wtf import Form
from wtforms import SelectField
from bs4 import BeautifulSoup


from secrets import API_KEY



cache.make_path()
yelp_covid.make_path()
path = './database/db.sqlite'
db = database.database(path)

class SelectForm(Form):
    country = SelectField('Country', choices=[
        ('us','USA'),('gb','Great Britain'),('ru','Russia')])


# exit()



# r = requests.get(business_search_url, headers=headers, params=params)
# data = json.loads(r.text)

# hello = restaurant.restaurant(json=data['businesses'][0])


app = Flask(__name__)

# app.config.from_object('config')
# curCategory = ''
# curCategoryList = []
# curCategoryList_str = []

# @app.route('/new')
# def new():
#     form = SelectForm()
#     return render_template('new.html', form = form )

@app.route('/')
def index():
    print('[FLASK]->index: --------------------------------------------------------')
    print('[FLASK]->index:')
    print('[FLASK]->index: --------------------------------------------------------')
    return render_template('index.html',states=db.get_states_information(), cities=[])

@app.route('/state', methods=['POST'])
def state():
    state_id = request.form.get('state')
    print('[FLASK]->state: --------------------------------------------------------')
    print('[FLASK]->state:                  [state_id]-> '+state_id)
    print('[FLASK]->state: --------------------------------------------------------')
    return render_template('state.html', states=db.get_states_information(), cities=db.get_cities_both_information_by_state_id(state_id), state_id=state_id)

@app.route('/city', methods=['POST'])
def city():
    
    city_id = request.form.get('city')
    state_id = db.get_state_id_by_city_id(city_id)
    curCity = db.get_city_name_by_city_id(city_id)
    curState = db.get_state_name_by_city_id(city_id)
    
    bar1, bar2, xvals, xvals_str= yelp_fusion.create_average_rating_and_count_graph_with_data(curCity, db, False)
    search_index = db.insert_search_info(city_id, db.get_state_id_by_city_id(city_id), xvals, xvals_str)
    curCategory = []
    for category in xvals:
        curCategory.append(str(search_index) + '_' + category)
    print('[FLASK]->city: ---------------------------------------------------------')
    print('[FLASK]->city:                   [state_id]-> '+state_id)
    print('[FLASK]->city:                   [state_name]-> '+curState)
    print('[FLASK]->city:                   [city_id]-> '+city_id)
    print('[FLASK]->city:                   [city_name]-> '+curCity)
    print('[FLASK]->city:                   [search_index]-> '+ str(search_index))
    print('[FLASK]->city: ---------------------------------------------------------')
    return render_template('city.html', states=db.get_states_information(), city_id=city_id, cities=db.get_cities_both_information_by_state_id(state_id), state_id=state_id, categories=curCategory, categories_str=xvals_str, total=range(len(xvals)), curCategory='', plot1=bar1, plot2=bar2)

@app.route('/table', methods=['POST'])
def table():
    category_index = request.form.get('category')
    print(category_index)
    search_index, category = category_index.split('_')
    city_id, state_id = db.get_city_and_state_by_search_index(search_index)
    curCity = db.get_city_name_by_city_id(city_id)
    curState = db.get_state_name_by_city_id(city_id)
    categories = db.get_category_by_search_index(search_index)
    curCategory_str = db.get_category_str_by_search_index(search_index)
    curCategory = []
    for ele in categories:
        curCategory.append(search_index + '_' + ele)
    category_alias = db.get_category_alias_by_category_title(category)
    table_basic_info = db.get_restaurant_table_by_category_and_city(curCity, category_alias) 
    covid_info = yelp_covid.make_info_readable(table_basic_info)
    city_location = db.get_city_location_by_city_id(city_id)
    restaurant_locations_data = db.get_restaurant_location_and_name_by_category_and_city(curCity, category_alias)
    time_stamp = yelp_covid.get_map(city_location, restaurant_locations_data)
    print('[FLASK]->table: --------------------------------------------------------')
    print('[FLASK]->table:                  [state_id]-> '+state_id)
    print('[FLASK]->table:                  [state_name]-> '+curState)
    print('[FLASK]->table:                  [city_id]-> '+city_id)
    print('[FLASK]->table:                  [city_name]-> '+curCity)
    print('[FLASK]->table:                  [search_index]-> '+ search_index)
    print('[FLASK]->table:                  [category]-> '+ category)
    print('[FLASK]->table:                  [category_alias]-> '+category_alias)
    print('[FLASK]->table:                  [category_alias]-> '+curCity)
    print('[FLASK]->table: --------------------------------------------------------')
    return render_template('table.html', states=db.get_states_information(), city_id=city_id, cities=db.get_cities_both_information_by_state_id(state_id), state_id=state_id, categories=curCategory, categories_str=curCategory_str, total=range(len(curCategory)), curCategory=category_index, table_basic_info=table_basic_info, table_len=len(table_basic_info), covid_info=covid_info, time_stamp=time_stamp)


@app.route('/maps/<id>')
def show_map(id):
    print('[FLASK]->map: ----------------------------------------------------------')
    print('[FLASK]->map:                    [map_id]-> ' + id)
    print('[FLASK]->map: ----------------------------------------------------------')
    return send_file('./maps/' + str(id) + '.html')


@app.route('/details/<id>')
def details(id):
    text = yelp_fusion.details(id, db)
    print('[FLASK]->details: ------------------------------------------------------')
    print('[FLASK]->details:                [restaurant_id]-> ' + id)
    print('[FLASK]->details: ------------------------------------------------------')
    return render_template('details.html', details=text)


# @app.route('/list/<uid>')
# def my_list(uid):
#     print('[FLASK]->list: ---------------------------------------------------------')
#     print(uid)
#     return url_for("my_list", uid=1, id=2, id2=3)


# @app.context_processor
# def override_url_for():
#     return dict(url_for=dated_url_for)


# def dated_url_for(endpoint, **values):
#     filename = None
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#     if filename:
#         file_path = os.path.join(app.root_path, endpoint, filename)
#         values['v'] = int(os.stat(file_path).st_mtime)
#     return url_for(endpoint, **values)

# @app.route('/map')
# def map():
#     start_coords = (46.9540700, 142.7360300)
#     folium_map = folium.Map(location=start_coords, zoom_start=14)
#     folium_map.save('templates/map.html')
#     return render_template('test.html')

# @app.route('/name/<nm>')  
# def name_nm(nm):
#     return render_template('name.html', name=nm)

# @app.route('/headlines/<nm>')
# def headlines_nm(nm):
#     url = 'https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=xeFKNh4VSVnb3NXLeVacjQZaBM8GW5js'
#     r = requests.get(url)
#     topFive = json.loads(r.text)['results'][0:6]
#     titles = []
#     for ele in topFive:
#         titles.append(ele['title'])
#         urls.append(ele['url'])
#     return render_template('headlines.html', name=nm, titles=titles)

# @app.route('/links/<nm>')
# def links_nm(nm):
#     url = 'https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=xeFKNh4VSVnb3NXLeVacjQZaBM8GW5js'
#     r = requests.get(url)
#     topFive = json.loads(r.text)['results'][0:6]
#     titles = []
#     urls = []
#     for ele in topFive:
#         titles.append(ele['title'])
#         urls.append(ele['url'])
#     return render_template('links.html', name=nm, titles=titles, urls=urls)

# @app.route('/images/<nm>')
# def images_nm(nm):
#     url = 'https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=xeFKNh4VSVnb3NXLeVacjQZaBM8GW5js'
#     r = requests.get(url)
#     topFive = json.loads(r.text)['results'][0:6]
#     titles = []
#     urls = []
#     imgs = []
#     for ele in topFive:
#         titles.append(ele['title'])
#         urls.append(ele['url'])
#         imgs.append(ele['multimedia'][0]['url'])
#     return render_template('images.html', name=nm, titles=titles, urls=urls, imgs=imgs)

if __name__ == '__main__':
    print('starting Flask app', app.name) 
    app.run(debug=True)

