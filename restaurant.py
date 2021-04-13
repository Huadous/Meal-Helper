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
    def __init__(self, name = "", category = "", star = 0.0, phone = "", hours = {}, location = "", url_location = "", url_yelp= "", url_real = ""):
        self.name = name
        self.category = category
        self.star = star
        self.phone = phone
        self.hours = hours
        self.location = location
        self.url_location = url_location
        self.url_yelp = url_yelp
        self.url_real = url_real
        self.covid_service = covid_19_service.Covid19Service()

    def updateRestaurantInfoByAPI(self, dic):
        bRestaurantInfo = False
        now = datetime.datetime.now()
        

    def updateRestaurantInfoByScraping(self, url):
        bRestaurantInfo = False
        bYelpPages = False
        now = datetime.datetime.now()
        try:
            with open("./cache/restaurant_info/" + url.replace('.','_').replace('/','&') + '.json', 'r') as f:
                text = f.read()
                print("Using Cache : restaurant_info")
                data = json.loads(text)
                if not ("time" in data and "html" in data):
                    raise()
                d = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                if (now - d).seconds / 3600 > 2.0:
                    raise()

                self.name = data['element']['name']
                self.category = data['element']['category']
                self.star = data['element']['star']
                self.phone = data['element']['phone']
                self.hours = data['element']['hours']
                self.location = data['element']['location']
                self.url_location = data['element']['url_location']
                self.url_yelp = data['element']['url_yelp']
                self.url_real = data['element']['url_real']
        except:
            bRestaurantInfo = True
            try:
                with open("./cache/yelp_pages/" + url.replace('.','_').replace('/','&') + '.json', 'r') as f:
                    text = f.read()
                    print("Using Cache : yelp_pages")
                    data = json.loads(text)
                    if not ("time" in data and "html" in data):
                        raise()
                    d = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                    if (now - d).seconds / 3600 > 2.0:
                        raise()
                    text = data["html"]
            except:
                bYelpPages = True
                print("Fetching")
                r = requests.get(url)
                text = r.text
            
        soup = BeautifulSoup(text, 'html.parser')
        self.covid_service.updateCovid19Info(url)
        self.name = soup.find('h1', class_ = "css-11q1g5y").contents[0]
        self.category = soup.find_all('span', class_="display--inline__373c0__3JqBP margin-r1__373c0__zyKmV border-color--default__373c0__3-ifU")[2].find('a').contents[0]
        self.star = float(soup.find('div', class_ = "arrange__373c0__2C9bH gutter-1-5__373c0__2vL-3 vertical-align-middle__373c0__1SDTo margin-b2__373c0__abANL border-color--default__373c0__3-ifU").find('div', role = "img")['aria-label'].split(' ')[0])
        self.phone = soup.find_all('div', class_ = "css-1vhakgw border--top__373c0__3gXLy border-color--default__373c0__3-ifU")[1].find('p', class_="css-1h1j0y3").contents[0]
        date = soup.find_all('th', class_ = "table-header-cell__373c0__OywTx")
        date_time = soup.find_all('p', class_ = "no-wrap__373c0__2vNX7 css-1h1j0y3")
        self.hours = {d.find('p').contents[0] : dt.contents[0] for d,dt in zip(date, date_time)}
        data = data = soup.find('address').find_all('span')
        self.location = data[0].contents[0] + ', ' + data[1].contents[0]
        self.url_location = "https://www.yelp.com" + soup.find_all('div', class_ = "css-1vhakgw border--top__373c0__3gXLy border-color--default__373c0__3-ifU")[2].find('a')['href']
        self.url_yelp = url
        self.url_real = soup.find_all('div', class_ = "css-1vhakgw border--top__373c0__3gXLy border-color--default__373c0__3-ifU")[0].find('a').contents[0]
        # make yelp pages as cache
        if bRestaurantInfo:
            data_yelp_pages_json = {"time" : str(now)[0:19], "html" : text}
            with open("./cache/yelp_pages/" + url.replace('.','_').replace('/','&') + '.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(data_yelp_pages_json, indent = 4, ensure_ascii = False))
            element = {
                'name' : self.name,
                'category' : self.category,
                'star' : self.star,
                'phone' : self.phone,
                'hours' : self.hours,
                'location' : self.location,
                'url_location' : self.url_location,
                'url_yelp' : self.url_yelp,
                'url_real' : self.url_real,
            }
        #make restaurant info as cache
        if bYelpPages:
            data_restaurant_info_json = {"time" : str(now)[0:19], "element" : element}
            with open("./cache/restaurant_info/" + url.replace('.','_').replace('/','&') + '.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(data_restaurant_info_json, indent = 4, ensure_ascii = False))

    def linkToDatabase(self, database):
        pass
            

    def showStatus(self):
        print("Covid 19 Services:")
        self.covid_service.showStatus()
        print("name : " + self.name)
        print("category : " + self.category)
        print("star : "  + str(self.star))
        print("phone : " + self.phone)
        print("hours : ")
        for i in self.hours.keys():
            print(i + " : " + self.hours[i])
        print("location : " + self.location)
        print("url_location : " + self.url_location)
        print("url_yelp : " + self.url_yelp)
        print("url_real : " + self.url_real)



