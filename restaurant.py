import covid_19_service
import datetime
import requests
import json
import sqlite3

from bs4 import BeautifulSoup

class restaurant:
    '''
    this class is what I try to describe the information get from the web

    '''

    def __init__(self, id='', json=''):
        if id == '' and json != '':
            self.id = json['id']
            self.alias = json['alias']
            self.name = json['name']
            self.image_url = json['image_url']
            self.is_closed = json['is_closed']
            self.url = json['url']
            self.review_count = json['review_count']
            self.categories = json['categories']
            self.rating = json['rating']
            self.coordinates_latitude = json['coordinates']['latitude']
            self.coordinates_longitude = json['coordinates']['longitude']
            self.transactions = json['transactions']
            self.price = json['price']
            self.location = json['location']
            self.phone = json['phone']
            self.display_phone = json['display_phone']
            self.save_cache(json)
            
        elif id !='':
            self.id = id
            contents = self.load_cache()

            if contents != {}:
                if self.check_time():
                    cache = self.remove_time_stamp(contents)
                    self.id = cache['id']
                    self.alias = cache['alias']
                    self.name = cache['name']
                    self.image_url = cache['image_url']
                    self.is_closed = cache['is_closed']
                    self.url = cache['url']
                    self.review_count = cache['review_count']
                    self.categories = cache['categories']
                    self.rating = cache['rating']
                    self.coordinates_latitude = cache['coordinates']['latitude']
                    self.coordinates_longitude = cache['coordinates']['longitude']
                    self.transactions = cache['transactions']
                    self.price = cache['price']
                    self.location = cache['location']
                    self.phone = cache['phone']
                    self.display_phone = cache['display_phone']
        else:
            self.id = ''
            self.alias = ''
            self.name = ''
            self.image_url = ''
            self.is_closed = True
            self.url = ''
            self.review_count = 0
            self.categories = ''
            self.rating = 0.0
            self.coordinates_latitude = 0.0
            self.coordinates_longitude = 0.0
            self.transactions = ''
            self.price = ''
            self.location = ''
            self.phone = ''
            self.display_phone = ''
        self.showStatus()
        self.covid_service = covid_19_service.Covid19Service()

    def load_cache(self):
        try:
            cache_file = open("./cache/restaurant_info/" + self.id + '.json', 'r')
            cache_file_contents = cache_file.read()
            cache = json.loads(cache_file_contents)
            cache_file.close()
        except:
            cache = {}
        return cache

    def save_cache(self, contents):
        cache_file = open("./cache/restaurant_info/" + self.id + '.json', 'w')
        contents_to_write = json.dumps(self.add_time_stamp(contents))
        cache_file.write(contents_to_write)
        cache_file.close()

    def add_time_stamp(self, contents):
        now = datetime.datetime.now()
        contents_with_time = {"time" : str(now)[0:19], "cache" : contents}
        return contents_with_time

    def remove_time_stamp(self, contents):
        return contents['cache']

    def check_time(self, contents):
        now = datetime.datetime.now()
        d = datetime.datetime.strptime(contents['time'], '%Y-%m-%d %H:%M:%S')
        if (now - d).seconds / 3600 > 2.0:
            return False
        return True

    def SyncDatabase(self, database):
        pass
            

    def showStatus(self):
        # print("Covid 19 Services:")
        # self.covid_service.showStatus()
        print("id : " + self.id)
        print("alias : " + self.alias)
        print("name : "  + str(self.name))
        print("image_url : " + self.image_url)
        print("is_closed : " + str(self.is_closed))
        print("url : " + self.url)
        print("review_count : " + str(self.review_count))
        print("categories : " + str(self.categories))
        print("rating : " + str(self.rating))
        print("coordinates_latitude : " + str(self.coordinates_latitude))
        print("coordinates_longitude : " + str(self.coordinates_longitude))
        print("transactions : " + str(self.transactions))
        print("price : " + self.price)
        print("location : " + str(self.location))
        print("phone : " + self.phone)
        print("display_phone : " + self.display_phone)        



