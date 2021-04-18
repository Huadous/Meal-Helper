import json
import datetime
import os

default_period = 2.0

def make_path():
    if not os.path.exists(r'./cache/categories'):
        os.makedirs(r'./cache/categories')
    if not os.path.exists(r'./cache/locations'):
        os.makedirs(r'./cache/locations')
    if not os.path.exists(r'./cache/covid_services'):
        os.makedirs(r'./cache/covid_services')
    if not os.path.exists(r'./cache/restaurant_search'):
        os.makedirs(r'./cache/restaurant_search')

def load_cache(name, type):
        try:
            cache_file = open("./cache/" + type + "/" + name.replace('/', '_') + '.json', 'r')
            cache_file_contents = cache_file.read()
            cache = json.loads(cache_file_contents)
            cache_file.close()
        except:
            cache = {}
        return cache

def save_cache(name, type, contents):
    cache_file = open("./cache/" + type + "/" + name.replace('/', '_') + '.json', 'w')
    contents_to_write = json.dumps(add_time_stamp(contents))
    cache_file.write(contents_to_write)
    cache_file.close()

def add_time_stamp(contents):
    now = datetime.datetime.now()
    contents_with_time = {"time" : str(now)[0:19], "cache" : contents}
    return contents_with_time

def remove_time_stamp(contents):
    return contents['cache']

def check_time(contents):
    now = datetime.datetime.now()
    d = datetime.datetime.strptime(contents['time'], '%Y-%m-%d %H:%M:%S')
    if (now - d).seconds / 3600 > default_period:
        return False
    return True

def sync_cache(name, type):
    contents = load_cache(name, type)
    if contents != {}:
        if check_time(contents):
            return remove_time_stamp(contents)
    return {}