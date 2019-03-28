"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

headers - Dictionary with headers to be used in requests.get function
xpath_category - Dictionary with xpaths for every element scrapped from th url / every category use the same dictionary

downloadPOI - Function
    Download data from maps.me and returns a python dictionary

saveJSON - Function
    Saves every category dictionary in a JSON file named by "country_locality" and "category"

saveNDJSON - Function
    Saves every category dictionary in a NDJSON file named by "cityname"

ingestdatatoelasticsearch - Function
    Ingests data into elasticsearch index

sendmessagetokafka - Function
    Sends a message to a KAFKA topic that new data are ingested into a kibana index
"""
import datetime
import os
import time
import urllib.request

import PIL.Image
import pytesseract
import requests
from lxml import html

DEBUG = True

headers = {
    'User-Agent': 'Mozilla/5.0',  # required
}

xpath_category = {
    #  xpath to find result number
    "url_paggination": "//ul[@class='pagination']//text()",

    #  xpath to get title url - on every result page
    "xpath_poi_title_url": "//div[@class='search-results-list-2']/article[@class='search-result-position']/div[@class='row'][2]/node()/div[@class='search-result-footer-6']/a//@href",

    # xpath to get all property description
    "xpath_poi_desc_address": "//span[@class='detail-info-subtitle']/a/text()",
    "xpath_poi_price": "//strong[@class='detail-info-price pull-right-sm']/img/@src",

    "xpath_poi_features_titles": "//div[@class='detail-article-content']/table[@class='table']/tbody/tr/th//text()",
    "xpath_poi_features_values": "//div[@class='detail-article-content']/table[@class='table']/tbody/tr[]/td/text()",
}


def downloadPOI(url_API, purpose, uniqueid_pattern):
    print("[+] Downloading data from immoscoop.be:", (purpose, url_API))

    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month)

    # first find how many pages there are for this category
    try:
        page = requests.get(url_API, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return False

    #  return how many results where found
    poi_pages = int(html.fromstring(page.text).xpath(xpath_category['url_paggination'])[-4])
    print("[+] Pages found: " + str(poi_pages))
    page_counter = 1  # starts at 1
    pois = {}
    poi_ascending_counter = 0

    while page_counter <= poi_pages:

        time.sleep(5)  # comment this line to be more aggressive

        url_API_next_page = url_API + str(page_counter)
        if DEBUG:
            print("[+] Downloading page: " + url_API_next_page)
        # request url
        try:
            next_page = requests.get(url_API_next_page, headers=headers)
        except requests.exceptions.RequestException as e:
            print(e)
            return False

        # take all poi urls from the page
        tree = html.fromstring(next_page.text)
        poi_titles_urls = tree.xpath(xpath_category['xpath_poi_title_url'])
        if not poi_titles_urls:  # check if there are results
            print("[+] No results found")
            return pois  # return an everything until that moment

        #  for every scraped page, get pois info
        for poi_counter in range(len(poi_titles_urls)):
            poi_url = poi_titles_urls[poi_counter]

            # download staff for url
            # request poi url
            time.sleep(2)  # comment to be more aggressive
            if DEBUG:
                print("\t[+] Downloading poi from: ", str(poi_url))
            try:
                poi_page = requests.get(str(poi_url), headers=headers)
            except requests.exceptions.RequestException as e:
                print(e)
                return False

            # for every poi, take its location (latitude, longitude)
            # save everything to the pois dictionary
            tree = html.fromstring(poi_page.text)

            #take postcode and category from URL
            poi_desc_postalcode = poi_url.split("/")[-4]
            poi_desc_category = poi_url.split("/")[-5]

            # take address from xpath - if not set it to '-'
            poi_desc_address = tree.xpath(xpath_category['xpath_poi_desc_address'])
            poi_desc_address = '-' if len(poi_desc_address) == 0 else poi_desc_address[0]

            # take price from xpath find price with image processing
            #pytesseract.pytesseract.tesseract_cmd = 'myenv/bin/pytesseract'
            #pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
            #TESSDATA_PREFIX = 'myenv/bin'
            #TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'

            poi_price_image_url_list = tree.xpath(xpath_category['xpath_poi_price'])  # image URL based on xpath
            if poi_price_image_url_list:
                poi_price_image_url = poi_price_image_url_list[0]
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Referer', poi_url)]  # use referer to take pic
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(poi_price_image_url, "price.png") #save at price.png

                #open price.png to extract number
                #price = pytesseract.image_to_string(PIL.Image.open('price.png').convert("RGB"), lang='eng', config='--psm 13 --eom 3 -c tessedit_char_whitelist=€0123456789')
                price = pytesseract.image_to_string(PIL.Image.open('price.png').convert("RGB"), lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=€0123456789')
#                print("PRICE:", price)
                if price != "":
                    poi_price = price.replace("€", "").replace(".", "").replace(" ", "").replace("O", "0").replace("—", "")
                    poi_price = float(poi_price)
                else:
                    poi_price = 0.0
            else: # Price upon request
                poi_price = 0.0
            # take Living Area from xpath and calculate price per sqm
            poi_features_titles = tree.xpath(xpath_category['xpath_poi_features_titles'])
            if "Living Area" in poi_features_titles:
                index = poi_features_titles.index('Living Area') + 1  # in which place of the table the Living Area is

                temp_xpath_poi_features_values = xpath_category['xpath_poi_features_values']
                temp_xpath_poi_features_values = temp_xpath_poi_features_values.replace("[]", "[" + str(index) + "]")
                poi_living_area = float(tree.xpath(temp_xpath_poi_features_values)[0].replace(" ", "")
                                        .replace("m", "").replace(".", "").replace(",", "").replace("\r", "")
                                        .replace("\n", "").replace("1ste:", ""))
                poi_price_per_sm = poi_price/poi_living_area

            else:
                poi_living_area = 0
                poi_price_per_sm = 0
            print(poi_price, poi_living_area)

            if "Construction Year" in poi_features_titles:
                index = poi_features_titles.index('Construction Year') + 1  # in which place of the table the Living Area is

                temp_xpath_poi_features_values = xpath_category['xpath_poi_features_values']
                temp_xpath_poi_features_values = temp_xpath_poi_features_values.replace("[]", "[" + str(index) + "]")
                poi_construction_year = int(tree.xpath(temp_xpath_poi_features_values)[0].replace(" ", "")
                                        .replace("m", "").replace(".", "").replace(",", "").replace("\r", "")
                                        .replace("\n", "").replace("1ste:", ""))

            else:
                poi_construction_year = 0

            '''
            print("Purpose", purpose)
            print("Postalcode:", poi_desc_postalcode)
            print("Category:", poi_desc_category)
            print("Address:", poi_desc_address)
            print("Price:", poi_price)
            print("Living Area:", poi_living_area)
            print("Price per sm:", poi_price_per_sm)
            '''

            poi = {"date": date, "purpose": purpose, "postcode": poi_desc_postalcode, "category": poi_desc_category,
                   "address": poi_desc_address, "price_per_sqr_met": poi_price_per_sm,
                   "construction_year": poi_construction_year}
            pois[uniqueid_pattern + str(poi_ascending_counter)] = poi
            poi_ascending_counter += 1

            #break
        #break

        page_counter += 1

    if DEBUG:
        print("[+] Found:", len(pois))

    # save results in csv also
    #with open('spitogatos_results/' + uniqueid_pattern + '.csv', 'w', newline='', encoding='utf8') as f:
    #    for key in pois.keys():
    #        f.write("%s,%s\n" % (key, pois[key]))

    # for key, value in pois.items():
    # print(key, value)

    return pois


def saveNDJSON(dictionary, poi_counter):
    if DEBUG:
        print("[+] Saving results in ndjson file")

    # create a directory if doesn't exists
    results_directory = "immoscoop_results/"
    results_filename = results_directory + "immoscoop.json"
    if not os.path.exists(results_directory):
        if DEBUG:
            print("[+] Creating results\' directory:", results_directory)
        os.makedirs(results_directory)

    print("[+] Saving file", results_filename)
    with open(results_filename, 'a', encoding='utf8') as fp:
        for key, value in dictionary.items():
            fp.write('{"index":{"_id":' + str(poi_counter) + '}}\n')
            value_str = str(value)  # .encode('utf-8')
            value_str = str(value_str).replace("\'", "\"") + "\n"
            fp.write(value_str)
            poi_counter += 1
    return poi_counter


def ingestdatatoelasticsearch(dictionary, index_name):
    from elasticsearch_functions import send_to_elasticsearch

    #index_name = "immoscoop-test"

    if DEBUG:
        print("[+] Ingesting results into elasticsearch - Index: " + index_name)

    send_to_elasticsearch(index_name, dictionary, '_doc')

def sendmessagetokafka(message, cityname):
    from kafka_functions import kafkasendmessage

    citynames = {"antwerp": "ANW"}
    topic = "DATA_" + citynames[cityname] + "_ECO_IMMOSCOOPEBE_CRAWLER"
    kafkasendmessage(topic, message)

