import requests
import datetime
import json

from bs4 import BeautifulSoup

class Covid19Service:
    '''
    this class is design to help add more information related to covid-19 for each restaurant

    '''

    def __init__(self, curbside_pickup = None, sit_down_dining = None, delivery = None, takeout = None, outdoor_seating = None, staff_wears_masks = None, social_distancing_enforced = None, masks_required = None, limited_capacity = None, staff_wears_gloves = None, sanitizing_between_customers = None, temperature_checks = None, hand_sanitizer_provided = None, contactless_payments = None):
        # Updated Service
        self.curbside_pickup = curbside_pickup
        self.sit_down_dining = sit_down_dining
        self.delivery = delivery
        self.takeout = takeout
        self.outdoor_seating = outdoor_seating
        # Health & Safety Measures
        self.staff_wears_masks = staff_wears_masks
        self.social_distancing_enforced = social_distancing_enforced
        self.masks_required = masks_required
        self.limited_capacity = limited_capacity
        self.staff_wears_gloves = staff_wears_gloves
        self.sanitizing_between_customers = sanitizing_between_customers
        self.temperature_checks = temperature_checks
        self.hand_sanitizer_provided = hand_sanitizer_provided
        self.contactless_payments = contactless_payments 
        self.other_service = {}

    def updateCovid19Info(self, url):
        self.other_service.clear()
        now = datetime.datetime.now()
        try:
            with open("./cache/covid_services/" + url.replace('.','_').replace('/','&') + '.json', 'r') as f:
                text = f.read()
                print("Using Cache : covid_services")
                data = json.loads(text)
                if not ("time" in data and "html" in data):
                    raise()
                d = datetime.datetime.strptime(data['time'], '%Y-%m-%d %H:%M:%S')
                if (now - d).seconds / 3600 > 2.0:
                    raise()
                self.curbside_pickup = data['element']['curbside_pickup']
                self.sit_down_dining = data['element']['sit_down_dining']
                self.delivery = data['element']['delivery']
                self.takeout = data['element']['takeout']
                self.outdoor_seating = data['element']['outdoor_seating']
                # Health & Safety Measures
                self.staff_wears_masks = data['element']['staff_wears_masks']
                self.social_distancing_enforced = data['element']['social_distancing_enforced']
                self.masks_required = data['element']['masks_required']
                self.limited_capacity = data['element']['limited_capacity']
                self.staff_wears_gloves = data['element']['staff_wears_gloves']
                self.sanitizing_between_customers = data['element']['sanitizing_between_customers']
                self.temperature_checks = data['element']['temperature_checks']
                self.hand_sanitizer_provided = data['element']['hand_sanitizer_provided']
                self.contactless_payments = data['element']['contactless_payments'] 
                self.other_service = data['element']['other_service']
        except:
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
                print("Fetching")
                r = requests.get(url)
                text = r.text
        soup = BeautifulSoup(text, 'html.parser')

        service_part = soup.find_all('div', class_ = "margin-t2__373c0__1CFWK border-color--default__373c0__3-ifU")[0:2]
        # margin-t2__373c0__1CFWK border-color--default__373c0__2oFDT
        for i in range(2):
            data = service_part[i].find_all('div', class_="display--inline-block__373c0__1ZKqC margin-r3__373c0__r37sx margin-b1__373c0__1khoT border-color--default__373c0__3-ifU")
            for ele in data:
                name = str(ele.find('span', class_ = "css-1h1j0y3").contents[0])
                status = bool(ele.find('span', attrs = {'aria-hidden' : 'true'})['class'][0] == 'icon--24-checkmark-v2')
                self.updateElement(name, status)
        # make yelp pages as cache
        data_yelp_pages_json = {"time" : str(now)[0:19], "html" : text}
        with open("./cache/yelp_pages/" + url.replace('.','_').replace('/','&') + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data_yelp_pages_json, indent = 4, ensure_ascii = False))

        # make covid services as cache
        element = {
            'curbside_pickup' : self.curbside_pickup, 
            'sit_down_dining' : self.sit_down_dining,
            'delivery' : self.delivery,
            'takeout' : self.takeout,
            'outdoor_seating' : self.outdoor_seating,
            'staff_wears_masks' : self.staff_wears_masks,
            'social_distancing_enforced' : self.social_distancing_enforced,
            'masks_required' : self.masks_required,
            'limited_capacity' : self.limited_capacity,
            'staff_wears_gloves' : self.staff_wears_gloves,
            'sanitizing_between_customers' : self.sanitizing_between_customers,
            'temperature_checks' : self.temperature_checks,
            'hand_sanitizer_provided' : self.hand_sanitizer_provided,
            'contactless_payments' : self.contactless_payments,
            'other_service' : self.other_service
        }
        data_covid_services_json = {"time" : str(now)[0:19], "element" : element}
        with open("./cache/covid_services/" + url.replace('.','_').replace('/','&') + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data_covid_services_json, indent = 4, ensure_ascii = False))

    def updateElement(self, name, status):
        name_lower = name.lower()
        if 'curbside pickup' in name_lower or 'curbside' in name_lower: 
            self.curbside_pickup = status
        elif 'sit-down dining' in name_lower or 'sit-down' in name_lower or 'sitdown' in name_lower:
            self.sit_down_dining = status
        elif 'delivery' in name_lower:
            self.delivery = status
        elif 'takeout' in name_lower:
            self.takeout = status
        elif 'outdoor seating' in name_lower:
            if not self.outdoor_seating:
                self.outdoor_seating = status
            if name_lower != 'outdoor seating':
                self.other_service[name_lower] = status
        elif 'staff wears masks' in name_lower:
            self.staff_wears_masks = status
        elif 'social distancing enforced' in name_lower or 'distancing' in name_lower:
            self.social_distancing_enforced = status
        elif 'masks required' in name_lower:
            self.masks_required = status
        elif 'limited capacity' in name_lower or 'limited' in name_lower:
            self.limited_capacity = status
        elif 'staff wears gloves' in name_lower or 'gloves' in name_lower:
            self.staff_wears_gloves = status
        elif 'sanitizing between customers' in name_lower:
            self.sanitizing_between_customers = status
        elif 'temperature checks' in name_lower:
            self.temperature_checks = status
        elif 'hand sanitizer provided' in name_lower:
            self.hand_sanitizer_provided = status
        elif 'contactless payments' in name_lower:
            self.contactless_payments = status
        else:
            self.other_service[name_lower] = status
    
    def showStatus(self):
        print("curbside_pickup : " + str(self.curbside_pickup))
        print("sit_down_dining : " + str(self.sit_down_dining))
        print("delivery : " + str(self.delivery))
        print("takeout : " + str(self.takeout))
        print("outdoor_seating : " + str(self.outdoor_seating))
        print("staff_wears_masks : " + str(self.staff_wears_masks))
        print("social_distancing_enforced : " + str(self.social_distancing_enforced))
        print("masks_required : " + str(self.masks_required))
        print("limited_capacity : " + str(self.limited_capacity))
        print("staff_wears_gloves : " + str(self.staff_wears_gloves))
        print("sanitizing_between_customers : " + str(self.sanitizing_between_customers))
        print("temperature_checks : " + str(self.temperature_checks))
        print("hand_sanitizer_provided : " + str(self.hand_sanitizer_provided))
        print("contactless_payments : " + str(self.contactless_payments))

        print("\nThere are " + str(len(self.other_service)) + " other services:")
        for ele in self.other_service.keys():
            print(ele + " :  " + str(self.other_service[ele]))