import requests
import sqlite3
import json
import restaurant
import plotly
import plotly.graph_objs as go
import database
import cache
import yelp_fusion

import pandas as pd
import numpy as np

from flask import Flask, render_template, request
from bs4 import BeautifulSoup

from secrets import API_KEY



cache.make_path()
path = './database/db.sqlite'
db = database.database(path)


# exit()



# r = requests.get(business_search_url, headers=headers, params=params)
# data = json.loads(r.text)

# hello = restaurant.restaurant(json=data['businesses'][0])


app = Flask(__name__)

@app.route('/')
def index():
    print(db.get_states_information())
    return render_template('index.html',states=db.get_states_information())

@app.route('/state', methods=['POST'])
def state():
    state_id = request.form.get('state')
    print(state_id)
    return render_template('state.html', states=db.get_states_information(), selected_state=state_id, cities=db.get_cities_information_by_state(state_id) )

@app.route('/city', methods=['POST'])
def city():
    city_id = request.form.get('city')
    print(city_id)
    # state_id = request.form.get('state')
    # print(state_id)
    bar = yelp_fusion.create_average_rating_graph(city_id, db)
    return render_template('city.html', states=db.get_states_information(), selected_city=city_id, cities=db.get_cities_information_by_state('IL'), plot=bar)

@app.route('/states')
def handle_the_form():
    bar = create_plot()
    return render_template('state.html', plot=bar)

@app.route('/name/<nm>')  
def name_nm(nm):
    return render_template('name.html', name=nm)

@app.route('/headlines/<nm>')
def headlines_nm(nm):
    url = 'https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=xeFKNh4VSVnb3NXLeVacjQZaBM8GW5js'
    r = requests.get(url)
    topFive = json.loads(r.text)['results'][0:6]
    titles = []
    for ele in topFive:
        titles.append(ele['title'])
        urls.append(ele['url'])
    return render_template('headlines.html', name=nm, titles=titles)

@app.route('/links/<nm>')
def links_nm(nm):
    url = 'https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=xeFKNh4VSVnb3NXLeVacjQZaBM8GW5js'
    r = requests.get(url)
    topFive = json.loads(r.text)['results'][0:6]
    titles = []
    urls = []
    for ele in topFive:
        titles.append(ele['title'])
        urls.append(ele['url'])
    return render_template('links.html', name=nm, titles=titles, urls=urls)

@app.route('/images/<nm>')
def images_nm(nm):
    url = 'https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=xeFKNh4VSVnb3NXLeVacjQZaBM8GW5js'
    r = requests.get(url)
    topFive = json.loads(r.text)['results'][0:6]
    titles = []
    urls = []
    imgs = []
    for ele in topFive:
        titles.append(ele['title'])
        urls.append(ele['url'])
        imgs.append(ele['multimedia'][0]['url'])
    return render_template('images.html', name=nm, titles=titles, urls=urls, imgs=imgs)

if __name__ == '__main__':
    print('starting Flask app', app.name) 
    app.run(debug=True)

