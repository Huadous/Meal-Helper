import requests
import sqlite3
import json
import restaurant
import plotly
import plotly.graph_objs as go
import database
import cache
import yelp_fusion
import copy

import pandas as pd
import numpy as np

from flask import Flask, render_template, request
from flask_wtf import Form
from wtforms import SelectField
from bs4 import BeautifulSoup


from secrets import API_KEY



cache.make_path()
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

curState = 'New York'
state_id = 'NY'
curCity = 'New York'
city_id = '1840034016'
# curCategory = ''
# curCategoryList = []
# curCategoryList_str = []


def copylist(new , old):
    new = []
    for i in range(len(old)):
        new.append(old[i])

# @app.route('/new')
# def new():
#     form = SelectForm()
#     return render_template('new.html', form = form )

@app.route('/')
def index():
    return render_template('index.html',states=db.get_states_information(), cities=db.get_cities_both_information_by_state_id(state_id), state_id=state_id, city_id=city_id)

@app.route('/state', methods=['POST'])
def state():
    state_id = request.form.get('state')
    print("****>" + curState)
    return render_template('index.html', states=db.get_states_information(), cities=db.get_cities_both_information_by_state_id(state_id), state_id=state_id, city_id='')

@app.route('/city', methods=['POST'])
def city():
    city_id = request.form.get('city')
    state_id = db.get_state_id_by_city_id(city_id)
    curCity = db.get_city_name_by_city_id(city_id)
    curState = db.get_state_name_by_city_id(city_id)
    print("----->" + curState)
    print(curCity)
    
    bar1, bar2, xvals, xvals_str= yelp_fusion.create_average_rating_and_count_graph_with_data(curCity, db, False)
    search_index = db.insert_search_info(city_id, db.get_state_id_by_city_id(city_id), xvals)
    curCategory = []
    for category in xvals:
        curCategory.append(str(search_index) + '_' + category)

    print(curCategory)
    return render_template('city.html', states=db.get_states_information(), city_id=city_id, cities=db.get_cities_both_information_by_state_id(state_id), state_id=state_id, categories=curCategory, categories_str=xvals_str, total=range(len(xvals)), curCategory='', plot1=bar1, plot2=bar2)

@app.route('/table', methods=['POST'])
def table():
    category_index = request.form.get('category')
    search_index, category = category_index.split('_')
    print("^^^^^^>" + search_index)
    print(db.get_city_and_state_by_search_index(search_index))
    print(db.get_city_name_by_city_id(city_id))
    print(db.get_state_name_by_city_id(city_id))
    city_id, state_id = db.get_city_and_state_by_search_index(search_index)[0]
    curCity = db.get_city_name_by_city_id(city_id)
    curState = db.get_state_name_by_city_id(city_id)
    curCategory = db.get_category_by_search_index(search_index)
    print(curCategory)
    return render_template('table.html', category=curCategory, states=db.get_states_information(), curCity=curCity, cities=db.get_cities_both_information_by_state_id(curState), curState=curState, categories=curCategory, categories_str=curCategoryList_str, total=range(len(curCategoryList)), curCategory=curCategory)

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

