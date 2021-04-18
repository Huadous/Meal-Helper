import json
import pprint
from csv import DictReader
import os

def csv_to_dict(path):
    try:
        with open(path, 'r') as f:
            dict_reader = DictReader(f)
            list_of_dict = list(dict_reader)
        return list_of_dict
    except IOError as err:
        print("I/O error({0})".format(err))