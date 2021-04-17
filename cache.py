import json
import datetime

default_period = 2.0

def load_cache(name, type):
        try:
            cache_file = open("./cache/" + type + "/" + name + '.json', 'r')
            cache_file_contents = cache_file.read()
            cache = json.loads(cache_file_contents)
            cache_file.close()
        except:
            cache = {}
        return cache

def save_cache(name, type, contents):
    cache_file = open("./cache/" + type + "/" + name + '.json', 'w')
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
    contents = cache.load_cache(name, type)
    if contents != {}:
        if cache.check_time(contents):
            return cache.remove_time_stamp(contents)
    return {}