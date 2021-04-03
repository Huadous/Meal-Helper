import requests
from bs4 import BeautifulSoup

from secrets import API_KEY


headers = {"Authorization": "Bearer {}".format(API_KEY)}
