import covid_19_service

class restaurant:
    '''
    this class is what I try to describe the information get from the web

    '''
    def __init__(self, name = "", category = "", star = 0.0, phone = "", hours = {}, location = "", url_yelp= "", url_real = ""):
        self.name = name
        self.category = category
        self.star = star
        self.phone = phone
        self.hours = hours
        self.location = location
        self.url_yelp = url_yelp
        self.url_real = url_real
        self.covid_service = covid_19_service()

    def updateRestaurantInfo(self, url):
        self.covid_service.updateCovid19Info(url_yelp)
        self.name = soup.find('h1', class_ = "css-11q1g5y").contents[0]
        self.category = soup.find_all('span', class_="display--inline__373c0__3JqBP margin-r1__373c0__zyKmV border-color--default__373c0__3-ifU")[2].find('a').contents[0]
        self.star = float(soup.find('div', class_ = "arrange__373c0__2C9bH gutter-1-5__373c0__2vL-3 vertical-align-middle__373c0__1SDTo margin-b2__373c0__abANL border-color--default__373c0__3-ifU")soup.find('div', class_ = "arrange__373c0__2C9bH gutter-1-5__373c0__2vL-3 vertical-align-middle__373c0__1SDTo margin-b2__373c0__abANL border-color--default__373c0__3-ifU").find('div', role = "img")['aria-label'].split(' ')[0])




