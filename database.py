
import requests
import sqlite3
import json

from flask import Flask, render_template
from bs4 import BeautifulSoup

from secrets import API_KEY


# PART 1: 
# loading the file(.json) downloads from Yelp Fusion which contains 
# categories, I filter the restaurant part and also load it into database
# WITHIN TABLE restaurantInfo.

with open("./src/category/restaurant_categories.json", 'r') as f:
    restaurant_categories = json.loads(f.read())

conn = sqlite3.connect("database/db.sqlite")
cur = conn.cursor()
DROP_OLD_TABLE_IF_EXISTS = '''
DROP TABLE IF EXISTS '''
cur.execute(DROP_OLD_TABLE_IF_EXISTS + 'restaurantInfo')

CREATE_RESTAURANT_CATEGORIES = '''
CREATE TABLE restaurantInfo(
	"title"	TEXT NOT NULL,
	"alias"	TEXT NOT NULL,
	"country_whitelist"	TEXT,
	"Id"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT)
);'''

cur.execute(CREATE_RESTAURANT_CATEGORIES)
INSERT_RESTAURANT_ITEM = '''
    INSERT INTO restaurantInfo
    VALUES (?, ?, ?, NULL)'''
for restaurant_type in restaurant_categories:
    if "country_blacklist" not in restaurant_type:
        cur.execute(INSERT_RESTAURANT_ITEM, [restaurant_type['title'], restaurant_type['alias'], 'NULL'])
        continue
    for country in restaurant_type["country_blacklist"]:
        cur.execute(INSERT_RESTAURANT_ITEM, [restaurant_type['title'], restaurant_type['alias'], country])

# PART 2:
# 1. Load the Country code follows ISO 3166-1 alpha-2 code. Also load it into database.
# Which may be used in the categories.
# WITHIN TABLE CountryCode
# 2. Load the information of US states and cities.
# WITHIN TABLE usStates AND usCities
with open("./src/location/data_json.txt", 'r') as f:
    country_code = json.loads(f.read())
cur.execute(DROP_OLD_TABLE_IF_EXISTS + 'CountryCode')

CREATE_COUNTRY_CODE = '''
CREATE TABLE CountryCode(
	"Code"	TEXT NOT NULL,
	"Name"	TEXT NOT NULL,
	"Id"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT)
);'''

cur.execute(CREATE_COUNTRY_CODE)
INSERT_COUNTRY_ITEM = '''
    INSERT INTO CountryCode
    VALUES (?, ?, NULL)'''
for country in country_code:
    cur.execute(INSERT_COUNTRY_ITEM, [country['Code'], country['Name']])

with open("./src/location/US_States_and_Cities.json", 'r') as f:
    us_states_and_cities = json.loads(f.read())

cur.execute(DROP_OLD_TABLE_IF_EXISTS + 'usStates')

CREATE_US_STATES_AND_CITIES = '''
CREATE TABLE usStatesAndCities(
	"State"	TEXT NOT NULL,
	"City"	TEXT NOT NULL,
	"Id"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT)
);'''

cur.execute(CREATE_US_STATES_AND_CITIES)
INSERT_RESTAURANT_ITEM = '''
    INSERT INTO usStatesAndCities
    VALUES (?, ?, NULL)'''
for state in us_states_and_cities.keys():
    for city in us_states_and_cities[state]:
        cur.execute(INSERT_RESTAURANT_ITEM, [state, city])

conn.commit()


