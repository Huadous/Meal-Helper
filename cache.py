import json
import datetime
import os

default_period = 2.0

def make_path():
    if not os.path.exists(r'./cache/categories'):
        os.makedirs(r'./cache/categories')
    print("[CACHE]->make_path:              [YES]-> './cache/categories'")
    if not os.path.exists(r'./cache/locations'):
        os.makedirs(r'./cache/locations')
    print("[CACHE]->make_path:              [YES]-> './cache/locations'")
    if not os.path.exists(r'./cache/covid_services'):
        os.makedirs(r'./cache/covid_services')
    print("[CACHE]->make_path:              [YES]-> './cache/categories'")
    if not os.path.exists(r'./cache/covid_services'):
        os.makedirs(r'./cache/restaurant_search')
    print("[CACHE]->make_path:              [YES]-> './cache/restaurant_search'")

def load_cache(name, type):
    try:
        cache_file = open("./cache/" + type + "/" + name.replace('/', '_') + '.json', 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
        print("[CACHE]->load_cache:             [YES]-> " + "./cache/" + type + "/" + make_name_readable(name))
    except:
        print("[CACHE]->load_cache:             [NO]-> " + "./cache/" + type + "/" + make_name_readable(name))
        cache = {}
    return cache

def make_name_readable(name):
    if len(name) > 50:
        return name[0:50] + '...'
    return name + '.json'

def save_cache(name, type, contents):
    cache_file = open("./cache/" + type + "/" + name.replace('/', '_') + '.json', 'w')
    contents_to_write = json.dumps(add_time_stamp(contents))
    cache_file.write(contents_to_write)
    cache_file.close()
    print("[CACHE]->save_cache:             [YES]-> " + "./cache/" + type + "/" + make_name_readable(name))

def add_time_stamp(contents):
    now = datetime.datetime.now()
    contents_with_time = {"time" : str(now)[0:19], "cache" : contents}
    print("[CACHE]->add_time_stamp:         [YES]-> " + contents_with_time['time'])
    return contents_with_time

def remove_time_stamp(contents):
    print("[CACHE]->remove_time_stamp:      [YES]-> " + contents['time'])
    return contents['cache']

def check_time(contents):
    now = datetime.datetime.now()
    d = datetime.datetime.strptime(contents['time'], '%Y-%m-%d %H:%M:%S')
    if (now - d).seconds / 3600 > default_period:
        print("[CACHE]->check_time:             [NO]-> " + "The cached data has expired.(default time limit: " + str(default_period) + " hour(s))")
        return False
    print("[CACHE]->check_time:             [YES]-> " + "The cached data has not expired.(default time limit: " + str(default_period) + " hour(s))")
    return True

def sync_cache(name, type):
    contents = load_cache(name, type)
    if contents != {}:
        if check_time(contents):
            print("[CACHE]->sync_cache:             [YES]-> " + "Synchronized successfully")
            return remove_time_stamp(contents)
    print("[CACHE]->sync_cache:             [NO]-> " + "Synchronized unsuccessfully")
    return {}