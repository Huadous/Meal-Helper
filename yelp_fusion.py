import requests
import json
import plotly
import plotly.graph_objs as go
import database
import cache

from secrets import API_KEY


yelp_fusion_business_search_url = 'https://api.yelp.com/v3/businesses/search'
headers = {"Authorization": "Bearer {}".format(API_KEY)}

def api_search(category, location, offset=0):
    print('[YELP_FUSION]->api_search:       [API]-> '+ category)
    file_name = category + '_' + location + '_' + str(offset)
    file_type = 'restaurant_search'
    api_search = cache.sync_cache(file_name, file_type)
    if api_search == {}:
        params = {
            'categories' : category, 
            'location' : location, 
            'offset' : offset,
            'limit' : 50,
            'sort_by' : 'rating'
            }
        r = requests.get(yelp_fusion_business_search_url, headers=headers, params=params)
        api_search = json.loads(r.text)
        cache.save_cache(file_name, file_type, api_search)
    return api_search

def api_search_all_data(category, location, db):
    LIMIT = 50
    cur = 0
    init_search = api_search(category, location, offset=cur)
    if 'error' in init_search:
        return []
    if init_search['total'] < LIMIT:
        LIMIT = init_search['total']
    data_collection = init_search['businesses']
    cur += 50
    while cur < LIMIT:
        data_collection.extend(api_search(category, location, offset=cur)['businesses'])
        cur += 50
        
    db.insert_restaurant_info(data_collection, category, location)
    return data_collection

def create_average_rating(category, city, db):
    return db.get_average_rating_by_category_and_city(category, city)

def details(id, db):
    text = db.get_restaurant_info_by_id(id)
    text = list(text)
    if len(text[12]) > 0:
        text[12] = text[12].replace('[', '<br>')
        text[12] = text[12].replace(']', '')
        text[12] = text[12].replace('{', '')
        text[12] = text[12].replace('}', '')
        text[12] = text[12].replace('"', '')
        text[12] = text[12].replace(',', '<br>')
    if len(text[10]) > 0:
        text[10] = text[10].replace('[', '')
        text[10] = text[10].replace(']', '')
        text[10] = text[10].replace('{', '')
        text[10] = text[10].replace('}', '')
        text[10] = text[10].replace('"', '')
        text[10] = text[10].replace(',', '<br>')
    return text

def create_average_rating_and_count_graph_with_data(city, db, dataonly=True): # city_name
    restaurant_category_all = db.get_restaurant_category_all()
    average_rating = []
    total_number = []
    
    for category in restaurant_category_all:
        api_search_all_data(category[0], city, db)
        average_rating_data, total_number_data = create_average_rating(category[0], city, db)
        average_rating.append(average_rating_data)
        total_number.append(total_number_data)
        print ("[YELP_FUSION]->create_average_rating_and_count_graph_with_data:      [{:3.0%}]".format(len(total_number)/len(restaurant_category_all)))
    xvals1 = []
    yvals1 = []
    xvals2 = []
    yvals2 = []
    for i in range(len(restaurant_category_all)):
        if average_rating[i] != None:
            yvals1.append(average_rating[i])
            xvals1.append(restaurant_category_all[i][1])
            yvals2.append(total_number[i])
            xvals2.append(restaurant_category_all[i][1])
    yvals1, xvals1 = zip(*sorted(zip(yvals1, xvals1),reverse=True))
    bar_data1 = [go.Bar(x=xvals1, y=yvals1)]
    yvals2, xvals2 = zip(*sorted(zip(yvals2, xvals2),reverse=True))
    bar_data2 = [go.Bar(x=xvals2, y=yvals2)]
    xvals_str = []
    for i in range(len(xvals1)):
        xvals_str.append(str(i + 1) + ". " + xvals1[i] + " : " + str(round(yvals1[i], 2)))
    if dataonly:
        return xvals1, xvals_str
    return json.dumps(bar_data1, cls=plotly.utils.PlotlyJSONEncoder), json.dumps(bar_data2, cls=plotly.utils.PlotlyJSONEncoder), xvals1, xvals_str
    

