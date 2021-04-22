import requests
import sqlite3
import json
import restaurant
import plotly
import plotly.graph_objs as go
import database
import cache
import re

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup


def visit_by_url(url):
    file_name = file_name_generator(url)
    file_type = 'covid_services'
    html_file = cache.sync_cache(file_name, file_type)
    if html_file == {} or len(html_file) == 0:
        r = requests.get(url)
        html_file = r.text
        cache.save_cache(file_name, file_type, html_file)
    return html_file

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
    print(url)
    soup = BeautifulSoup(html, 'html.parser')
    service_part = soup.find_all('div', class_ = re.compile('^margin-t2'))[0:2]
    print(len(service_part))
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
    return dataset
            
def make_info_readable(table_basic_info):
    covid_info = []
    for ele in table_basic_info:
        url = ele[1]
        dataset = get_covid_info(url)
        string_1 = ''
        string_2 = ''
        for ele in dataset[0]:
            string_1 += str(ele[0]) + ' : ' + str(ele[1]) + '<br>'
        for ele in dataset[1]:
            string_2 += str(ele[0]) + ' : ' + str(ele[1]) + '<br>'
        covid_info.append([string_1, string_2])
        print(string_1)
        print(string_2)
    return covid_info