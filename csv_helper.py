from csv import DictReader

def csv_to_dict(path):
    try:
        with open(path, 'r') as f:
            dict_reader = DictReader(f)
            list_of_dict = list(dict_reader)
        print("[CSV]->csv_to_dict:              [YES]-> " + "Load csv successfully")
        return list_of_dict
    except IOError as err:
        print("[CSV]->csv_to_dict:              I/O error({0})".format(err))