import requests
import sqlite3
import json
import restaurant
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np

from flask import Flask, render_template, request
from bs4 import BeautifulSoup

from secrets import API_KEY


headers = {"Authorization": "Bearer {}".format(API_KEY)}
params = {}
params['item'] = 'Chinese'
params['location'] = 'NYU'

business_search_url = 'https://api.yelp.com/v3/businesses/search'


r = requests.get(business_search_url, headers=headers, params=params)
data = json.loads(r.text)

hello = restaurant.restaurant(json=data['businesses'][0])


conn = sqlite3.connect("database/db.sqlite")
cur = conn.cursor()

query = '''
    SELECT DISTINCT State FROM usStatesAndCities
    '''
cur.execute(query)
result = []
for row in cur:
    result.append(row[0])
print(result)




def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',states = result)

@app.route('/state', methods=['POST'])
def state():
    state = request.form.get('state')
    return 

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

