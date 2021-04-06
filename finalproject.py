import requests
from bs4 import BeautifulSoup

from secrets import API_KEY


headers = {"Authorization": "Bearer {}".format(API_KEY)}
with open("./src/category/restaurant_categories.json", 'r') as f:
    restaurant_categories = json.loads(f.read())

