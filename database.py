import requests
import sqlite3
import json
import cache
import csv_helper
import os
import datetime

from distutils.util import strtobool
from flask import Flask, render_template
from bs4 import BeautifulSoup

from secrets import API_KEY


check_exists = lambda key, base : base[key] if key in base.keys() else 'NULL'
class database:
    '''
    '''
    def __init__(self, path):
        if not os.path.exists(r'./database'):
            os.makedirs(r'./database')
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cur = self.conn.cursor()
        # PART 1: 
        # loading the file(.json) downloads from Yelp Fusion which contains 
        # categories, I filter the restaurant part and also load it into database
        # WITHIN TABLE restaurantInfo.
        file_name = 'categories_information'
        file_type = 'categories'
        categories_information = cache.sync_cache(file_name, file_type)
        if categories_information == {} or len(categories_information) == 0:
            categories_information_url_json = 'https://www.yelp.com/developers/documentation/v3/all_category_list/categories.json'
            r = requests.get(categories_information_url_json)
            categories_information =json.loads(r.text)
            cache.save_cache(file_name, file_type, categories_information)
        
        file_name = 'restaurant_category_information'
        file_type = 'categories'
        restaurant_category_information = cache.sync_cache(file_name, file_type)
        if restaurant_category_information == {} or len(restaurant_category_information) == 0:
            restaurant_category_information = []
            for ele in categories_information:
                if 'parents' in ele and len(ele['parents']) > 0 and ele['parents'][0] == 'restaurants':
                    restaurant_category_information.append(ele)
            cache.save_cache(file_name, file_type, restaurant_category_information)

        CREATE_RESTAURANT_CATEGORY_INFORMATION = '''
        CREATE TABLE IF NOT EXISTS restaurant_category_information(
            "title"	TEXT NOT NULL,
            "alias"	TEXT NOT NULL,
            "country_whitelist"	TEXT
        );'''
        self.cur.execute(CREATE_RESTAURANT_CATEGORY_INFORMATION)

        INSERT_RESTAURANT_CATEGORY_INFORMATION = '''
            INSERT INTO restaurant_category_information
            VALUES (?, ?, ?)'''
        for restaurant_type in restaurant_category_information:
            if "country_blacklist" not in restaurant_type:
                self.cur.execute(INSERT_RESTAURANT_CATEGORY_INFORMATION, [restaurant_type['title'], restaurant_type['alias'], 'US'])
                continue
            for country in restaurant_type["country_blacklist"]:
                self.cur.execute(INSERT_RESTAURANT_CATEGORY_INFORMATION, [restaurant_type['title'], restaurant_type['alias'], country])

        # PART 2:
        # 1. Load the Country code follows ISO 3166-1 alpha-2 code. Also load it into database.
        # Which may be used in the categories.
        # WITHIN TABLE CountryCode
        # 2. Load the information of US states and cities.
        # WITHIN TABLE usStates AND usCities
        

        file_name = 'iso_3166_1_alpha_2_code'
        file_type = 'locations'
        iso_3166_1_alpha_2_code = cache.sync_cache(file_name, file_type)
        if iso_3166_1_alpha_2_code == {} or len(iso_3166_1_alpha_2_code) == 0:
            iso_3166_1_alpha_2_code_url_json = 'https://datahub.io/core/country-list/r/data.json'
            r = requests.get(iso_3166_1_alpha_2_code_url_json)
            iso_3166_1_alpha_2_code =json.loads(r.text)
            cache.save_cache(file_name, file_type, iso_3166_1_alpha_2_code)

        CREATE_ISO_3166_1_ALPHA_2_CODE = '''
        CREATE TABLE IF NOT EXISTS iso_3166_1_alpha_2_code(
            "Code"	TEXT NOT NULL,
            "Name"	TEXT NOT NULL,
            PRIMARY KEY("Code")
        );'''
        self.cur.execute(CREATE_ISO_3166_1_ALPHA_2_CODE)

        INSERT_ISO_3166_1_ALPHA_2_CODE = '''
        INSERT OR IGNORE INTO iso_3166_1_alpha_2_code
        VALUES (?, ?)'''
        for country in iso_3166_1_alpha_2_code:
            self.cur.execute(INSERT_ISO_3166_1_ALPHA_2_CODE, [country['Code'], country['Name']])


        source_path = './src/location/uscities.csv'
        file_name = 'us_cities'
        file_type = 'locations'
        us_cities = cache.sync_cache(file_name, file_type)
        if us_cities == {} or len(us_cities) == 0:
            us_cities = csv_helper.csv_to_dict(source_path)
            cache.save_cache(file_name, file_type, us_cities)

        CREATE_US_CITIES = '''
        CREATE TABLE IF NOT EXISTS us_states (
            "city"	TEXT,
            "city_ascii"	TEXT,
            "state_id"	TEXT,
            "state_name"	TEXT,
            "county_fips"	TEXT,
            "county_name"	TEXT,
            "lat"	REAL,
            "lng"	REAL,
            "population"	INTEGER,
            "density"	INTEGER,
            "source"	TEXT,
            "military"	INTEGER,
            "incorporated"	INTEGER,
            "timezone"	TEXT,
            "ranking"	INTEGER,
            "zips"	TEXT,
            "id"	TEXT,
            PRIMARY KEY("id")
        );'''

        self.cur.execute(CREATE_US_CITIES)
        INSERT_US_CITIES = '''
        INSERT OR REPLACE INTO us_states
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        for city in us_cities:
            insert_data = [
                city['city'],
                city['city_ascii'],
                city['state_id'],
                city['state_name'],
                city['county_fips'],
                city['county_name'],
                city['lat'],
                city['lng'],
                city['population'],
                city['density'],
                city['source'],
                int(strtobool(city['military'])),
                int(strtobool(city['incorporated'])),
                city['timezone'],
                city['ranking'],
                city['zips'],
                city['id']
            ]
            self.cur.execute(INSERT_US_CITIES, insert_data)

        CREATE_RESTAURANT_INFORMATION = '''
            CREATE TABLE IF NOT EXISTS "restaurant_information" (
                "id"	TEXT,
                "alias"	TEXT,
                "name"	TEXT,
                "image_url"	TEXT,
                "is_closed"	INTEGER,
                "url"	TEXT,
                "review_count"	INTEGER,
                "rating"	REAL,
                "coordinates_latitude"	REAL,
                "coordinates_longitude"	REAL,
                "transactions"	TEXT,
                "price"	TEXT,
                "location"	TEXT,
                "phone"	TEXT,
                "display_phone"	TEXT,
                PRIMARY KEY("id")
            );'''
        self.cur.execute(CREATE_RESTAURANT_INFORMATION)
        CREATE_RESTAURANT_CATEGORY_FETCH = '''
        CREATE TABLE IF NOT EXISTS restaurant_category_fetch (
            "id"	TEXT NOT NULL,
            "category"	TEXT NOT NULL,
            "city" TEXT NOT NULL,
            "time" TEXT NOT NULL
        );'''
        self.cur.execute(CREATE_RESTAURANT_CATEGORY_FETCH)
        CREATE_RESTAURANT_CATEGORY = '''
        CREATE TABLE IF NOT EXISTS restaurant_category (
            "id"	TEXT NOT NULL,
            "category"	TEXT NOT NULL,
            "city" TEXT NOT NULL,
            "unique_str" TEXT NOT NULL,
            PRIMARY KEY("unique_str")
        );'''
        self.cur.execute(CREATE_RESTAURANT_CATEGORY)
        CREATE_SEARCH_INDEX = '''
        CREATE TABLE IF NOT EXISTS search_index (
            "id"	INTEGER,
            "city_id"	TEXT NOT NULL,
            "state_id"	TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );'''
        self.cur.execute(CREATE_SEARCH_INDEX)
        CREATE_SEARCH_RESULTS = '''
        CREATE TABLE IF NOT EXISTS search_results (
            "id"	INTEGER,
            "search_index"	INTEGER NOT NULL,
            "category"	TEXT NOT NULL,
            "category_str" TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
        );'''
        self.cur.execute(CREATE_SEARCH_RESULTS)
        self.conn.commit()

    def insert_restaurant_info(self, restaurants, category, city):
        INSERT_RESTAURANT_INFORMATION = '''
        INSERT OR IGNORE INTO restaurant_information
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        INSERT_RESTAURANT_CATEGORY_FETCH = '''
        INSERT INTO restaurant_category_fetch
        VALUES (?, ?, ?, ?)'''
        INSERT_RESTAURANT_CATEGORY = '''
        INSERT OR REPLACE INTO restaurant_category
        VALUES (?, ?, ?, ?)'''
        for restaurant in restaurants:
            insert_data = [
                check_exists('id', restaurant),
                check_exists('alias', restaurant),
                check_exists('name', restaurant),
                check_exists('image_url', restaurant),
                int(check_exists('is_closed', restaurant)),
                check_exists('url', restaurant),
                check_exists('review_count', restaurant),
                check_exists('rating', restaurant),
                check_exists('coordinates', restaurant)['latitude'],
                check_exists('coordinates', restaurant)['longitude'],
                json.dumps(check_exists('transactions', restaurant)),
                check_exists('price', restaurant),
                json.dumps(check_exists('location', restaurant)),
                check_exists('phone', restaurant),
                check_exists('display_phone', restaurant),
            ]
            self.cur.execute(INSERT_RESTAURANT_INFORMATION, insert_data)
            for ele in restaurant['categories']:
                self.cur.execute(INSERT_RESTAURANT_CATEGORY, [check_exists('id', restaurant), ele['alias'], city, check_exists('id', restaurant) + '_' + ele['alias'] + '_' + city])
            for ele in restaurant['categories']:
                if category == ele['alias']:
                    self.cur.execute(INSERT_RESTAURANT_CATEGORY_FETCH, [check_exists('id', restaurant), category, city, str(datetime.datetime.now())[0:19]])
                    break

        self.conn.commit()

    def insert_search_info(self, city_id, state_id, categories, categories_str):
        INSERT_SEARCH_INDEX = '''
        INSERT INTO search_index
        VALUES (NULL, ?, ?)'''
        self.cur.execute(INSERT_SEARCH_INDEX, [city_id, state_id])
        SELECT_SEARCH_INDEX = '''
        SELECT DISTINCT last_insert_rowid() FROM search_index
        '''
        search_index = self.get_result(SELECT_SEARCH_INDEX, 1)
        INSERT_SEARCH_RESULTS = '''
        INSERT INTO search_results
        VALUES (NULL, ?, ?, ?)
        '''
        for i in range(len(categories)):
            self.cur.execute(INSERT_SEARCH_RESULTS, [search_index, categories[i], categories_str[i]])
        self.conn.commit()
        return search_index

    def get_category_by_search_index(self, search_index):
        SELECT_SEARCH_RESULTS = '''
        SELECT category FROM search_results
        WHERE search_index={}
        '''.format(search_index)
        return self.get_result(SELECT_SEARCH_RESULTS, 1)
    
    def get_category_str_by_search_index(self, search_index):
        SELECT_SEARCH_RESULTS = '''
        SELECT category_str FROM search_results
        WHERE search_index={}
        '''.format(search_index)
        return self.get_result(SELECT_SEARCH_RESULTS, 1)

    def get_city_and_state_by_search_index(self, search_index):
        SELECT_SEARCH_INDEX = '''
        SELECT city_id, state_id FROM search_index
        WHERE id={}
        '''.format(search_index)
        return self.get_result(SELECT_SEARCH_INDEX, 2)


    def get_states_information(self):
        SELECT_STATES_INFORMATION = '''
        SELECT DISTINCT state_name, state_id FROM us_states'''
        return self.get_result(SELECT_STATES_INFORMATION, 2)

    def get_cities_both_information_by_state_id(self, state_id):
        SELECT_CITIES_INFORMATION = 'SELECT DISTINCT city_ascii, id FROM us_states WHERE state_id == "{}"'.format(state_id)
        return self.get_result(SELECT_CITIES_INFORMATION, 2)

    def get_average_rating_by_category_and_city(self, category, city):
        CREATE_AVERAGE_RATING = '''
        SELECT avg(rating), count(restaurant_category.id)
        FROM restaurant_information
        JOIN restaurant_category ON restaurant_information.id = restaurant_category.id
        WHERE restaurant_category.category = '{}' AND restaurant_category.city = '{}'
        '''.format(category, city)
        return self.get_result(CREATE_AVERAGE_RATING, 2)

    def get_result(self, query, num):
        self.cur.execute(query)
        results = []
        if num == 0:
            return results
        for row in self.cur:
            if num == 1:
                results.append(row[0])
            else:
                results.append(row[0:num])

        if len(results) == 1:
            return results[0]
        return results

    def get_restaurant_category_all(self):
        SELECT_DISTINCT_RESTAURANT_CATEGORY = "SELECT DISTINCT alias, title FROM restaurant_category_information WHERE country_whitelist = 'US'"
        return self.get_result(SELECT_DISTINCT_RESTAURANT_CATEGORY, 2)

    def get_state_name_by_city_id(self, city):
        SELECT_STATE_NAME = 'SELECT state_name FROM us_states WHERE id == "{}"'.format(city)
        return self.get_result(SELECT_STATE_NAME, 1)
    
    def get_state_id_by_city_id(self, city):
        SELECT_STATE_ID = 'SELECT state_id FROM us_states WHERE id == "{}"'.format(city)
        return self.get_result(SELECT_STATE_ID, 1)

    def get_city_name_by_city_id(self, city_id):
        SELEECT_CITY_NAME = 'SELECT city_ascii FROM us_states WHERE id == "{}"'.format(city_id)
        return self.get_result(SELEECT_CITY_NAME, 1)

  