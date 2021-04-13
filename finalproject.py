import requests
import sqlite3
import json
from bs4 import BeautifulSoup

from secrets import API_KEY


headers = {"Authorization": "Bearer {}".format(API_KEY)}
with open("./src/category/restaurant_categories.json", 'r') as f:
    restaurant_categories = json.loads(f.read())

conn = sqlite3.connect("database/db.sqlite")
cur = conn.cursor()

CREATE_RESTAURANT_CATEGORIES = '''
CREATE TABLE IF NOT EXISTS restaurantInfo(
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



conn.commit()

