import re
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import googlemaps
import bs4
from datetime import datetime
import pandas as pd

class rdcParser:

    def __init__(self, url: str, gmaps_credentials: dict):
        self.url = url
        self.gmaps_credentials = gmaps_credentials
        self.baseurl = re.sub(r'(.+)(\/pg\-\d)', r'\1', self.url)
        self.gmaps = googlemaps.Client(key = self.gmaps_credentials['google_maps_api_key'])
        self.processed_urls = []
        if re.match(".*apartments.*", url):
            self.kind = "rent"
        else:
            self.kind = "buy"

    def getHTML(self):
        options = Options()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = options)

        # Scrape url and extract html with soup
        driver.get(self.url)
            
        soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        self.soup = soup

        driver.quit()
        # return soup

    def getLatLong(self, address):
        address = re.sub(",", "", address)
        response = self.gmaps.geocode(address)
        lat_long = response[0]['geometry']['location']
        return(lat_long)
    
    def extractAttributes(self, attr: list):
        property_dict = {}
        for item in attr:
            if item["data-testid"] == "card-price":
                property_dict["price"] = attr[0].string
            elif item["data-testid"] == "card-meta":
                try:
                    property_dict["beds"] = attr[1].find(attrs = {"data-testid" : "property-meta-beds"}).span.string
                except:
                    property_dict["beds"] = ""
                try:
                    property_dict["baths"] = attr[1].find(attrs = {"data-testid" : "property-meta-baths"}).span.string
                except:
                    property_dict["baths"] = ""
                try:   
                    property_dict["sqft"] = attr[1].find(attrs = {"data-testid" : "property-meta-sqft"}).find(attrs = {"data-testid": "meta-value"}).string
                except:
                    property_dict["sqft"] = ""
                try:
                    property_dict["lot"] = attr[1].find(attrs = {"data-testid" : "property-meta-lot-size"}).find(attrs = {"data-testid" : "meta-value"}).string
                except:
                    property_dict["lot"] = ""
            elif item["data-testid"] == "card-address":
                property_dict["address"] = ' '.join([x.string for x in attr[2].find_all(attrs = {"data-testid" : ["card-address-1", "card-address-2"]})])
                property_dict["zip"] = re.findall(r'\d{5}', property_dict['address'])[0]
                latitude_longitude = self.getLatLong(property_dict['address'])
                property_dict["Latitude"] = latitude_longitude['lat']
                property_dict["Longitude"] = latitude_longitude['lng']
        return property_dict
    
    def getData(self):
        card_content = self.soup.find_all(attrs = {"data-testid": "card-content"})
        property_data = {}
        for prop in card_content:
            property_attributes = prop.find_all(
                attrs = {
                    "data-testid" : ["card-address", "card-price", "card-meta"]
                }
            )
            property_attributes = self.extractAttributes(property_attributes)
            property_attributes['url'] = "https://www.realtor.com" + prop.a['href']
            property_attributes['date'] = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
            key = str(hash(property_attributes['address']))[1:13]
            property_data[key] = property_attributes
        self.data = property_data
        self.processed_urls.append(self.url)
    
    def getPages(self):
        pages = self.soup.find(attrs = {'aria-label' : "pagination"})
        a_list = pages.find_all('a')
        pg_nums = [tag.string for tag in a_list]
        max_pages = 0
        url_list = []
        for pg in pg_nums:
            try:
                page = int(pg)
                if page > max_pages:
                    max_pages = page
            except:
                continue
        for i in range(max_pages):
            if i == 0:
                continue
            new_url = self.baseurl + "/pg-" + str(i+1)
            url_list.append(new_url)
        self.pages = url_list.reverse()

    def cleanData(self):
        keys = pd.DataFrame(self.data.keys(), columns = ["id"])
        values = pd.DataFrame.from_dict(self.data.values())
        df = pd.concat([keys, values], axis = 1)
        if self.kind == "buy":
            df['price'] = df.price.apply(lambda x: float(re.sub("\$|,", "", x)))
            df['beds'] = df.beds.apply(lambda x: int(re.sub("\+", "", x.lower()).replace("studio", "0").strip() or -1))
            df['baths'] = df.baths.apply(lambda x: float(re.sub("\+", "", x.lower()).strip() or -1))
            df[['sqft', 'lot']] = df[['sqft','lot']].apply(lambda x: x.apply(lambda y: float(re.sub("\$|,", "", y) or -1)))
        elif self.kind == "rent":
            cols = df.columns
            for col in ['price', 'beds', 'baths', 'sqft']:
                df[[f'{col}_lower', f'{col}_upper']] = df[col].str.split('-', expand = True)
                df = df.drop(col, axis = 1)

            df = pd.wide_to_long(
                df, 
                stubnames = ['price', 'beds', 'baths', 'sqft'],
                i = 'id',
                j = 'bound',
                sep = "_",
                suffix = r'\w+'
            )

            df = df.reset_index().dropna(subset = 'price')
            df['price'] = df.price.apply(lambda x: float(re.sub("\$|,", "", x)))
            df['beds'] = df.beds.fillna("").apply(lambda x: int(re.sub("\W", "", x.lower()).replace("studio", "0").strip() or -1))
            df['baths'] = df.baths.fillna("").apply(lambda x: float(re.sub("\+", "", x.lower()).strip() or -1))
            df[['sqft']] = df[['sqft']].fillna("").apply(lambda x: x.apply(lambda y: float(re.sub("\$|,", "", y) or -1)))

            # Filter errant buy columns
            df = df[df.url.apply(lambda x: bool(re.match(r'.*rentals.*', x)))]

            # Reorder and drop
            df = df[cols]
            df = df.drop(["lot"], axis = 1)
        self.data = df