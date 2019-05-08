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

ingestdatatoelasticsearch - Function
    Ingests data into elasticsearch index

sendmessagetokafka - Function
    Sends a message to a KAFKA topic that new data are ingested into a kibana index
"""

import os
import time
import json
import requests
import datetime
from lxml import html

DEBUG = False

headers = {
    'User-Agent': 'Mozilla/5.0',  # required
}


xpath_category = {
    "url_API_next_page": 1,  # second page: 2, third page: 3 etc.
    "url_paggination": "//li[@class='pagination__item']/a/text()",
    "xpath_poi_title": "//div[@class='item__title']/a[@class='text__lg']/text()",
    "xpath_poi_title_url": "//div[@class='item__title']/a[@class='text__lg']//@href",
    "poi_url": "https://maps.me",
    "poi_location": "//div[@class='mm-object__desc'][1]/p[@class='item__desc-location']/span/text()"
}


def downloadPOI(element_xpath_dictionary, country_locality):

    #  create local variables url_API and url_API_next_page from element_xpath_dictionary
    url_API = element_xpath_dictionary['url_API'] + country_locality + "/?page="
    url_API_next_page = xpath_category['url_API_next_page']
    print("[+] Downloading data for:", element_xpath_dictionary['poi_name'])

    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month)

    # first find how many pages there are for this category
    try:
        page = requests.get(url_API + str(url_API_next_page), headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return False

    pages_for_poi = html.fromstring(page.text).xpath(xpath_category['url_paggination'])
    if not pages_for_poi:  # there is a case where there is only one page (without pagination)
        pages_for_poi = int(1)
    else:
        pages_for_poi = int(pages_for_poi[-1])
    if DEBUG:
        print("[+] Pages to scrape:", pages_for_poi)

    pois = {}
    #  while there are pages to scrape
    while url_API_next_page <= pages_for_poi:

        time.sleep(5)  # comment this line to be more aggressive
        if DEBUG:
            print("[+] Downloading page: " + url_API + str(url_API_next_page))

        # request url
        try:
            next_page = requests.get(url_API + str(url_API_next_page), headers=headers)
        except requests.exceptions.RequestException as e:
            print(e)
            return False

        # save everything to the pois dictionary
        tree = html.fromstring(next_page.text)
        poi_titles = tree.xpath(xpath_category['xpath_poi_title'])
        poi_titles_urls = tree.xpath(xpath_category['xpath_poi_title_url'])

        if not poi_titles:  # check if there are results
            if DEBUG:
                print("[+] No results found")
            return {}  # return an empty dictionary

        #  for every scraped page pois, download pois info
        for poi_counter in range(len(poi_titles)):
            poi_url = poi_titles_urls[poi_counter]

            # download staff for url
            # request poi url
            time.sleep(2)  # comment to be more aggressive
            if DEBUG:
                print("\t[+] Downloading poi from: ", xpath_category['poi_url'] + str(poi_url))
            try:
                poi_page = requests.get(xpath_category['poi_url'] + str(poi_url), headers=headers)
            except requests.exceptions.RequestException as e:
                print(e)
                return False

            # for every poi, take its location (latitude, longitude)
            # save everything to the pois dictionary
            tree = html.fromstring(poi_page.text)
            poi_location = tree.xpath(xpath_category['poi_location'])[0]
            poi_location = poi_location.split("GPS:")[1]
            poi_lat = poi_location.split(",")[0]
            poi_lon = poi_location.split(",")[1]
            poi_goe_point = str(poi_lat) + "," + str(poi_lon) #geo_point added

            #  create a new element in pois dictionary
            pois[poi_titles[poi_counter]] = {"poi_category": element_xpath_dictionary['poi_category'].replace("\'", ""),
                                             #"poi_name": poi_titles[poi_counter],
                                             #"poi_url": poi_titles_urls[poi_counter],
                                             #"poi_latitude": poi_lat, "poi_longitude": poi_lon,
                                             "poi_subcategory": element_xpath_dictionary['poi_name'].replace("\'", ""),
                                             "poi_geo_point": poi_goe_point,
                                             "date": date}

            #break #  uncomment to take only the first poi of the page
        #  scrape next page
        url_API_next_page += 1
        #break #  uncomment to take only the first page for the category

        # sleep 10 secs everytime you change category
        time.sleep(10)
    if DEBUG:
        print("[+] Found:", len(pois))

    #for key, value in pois.items():
    #    print(key, value)

    return pois


def saveJSON(dictionary, cityname, category):

    if DEBUG:
        print("[+] Saving results in json file")

    # create a directory if doesn't exists
    results_directory = "maps_me_results/"
    if not os.path.exists(results_directory):
        if DEBUG:
            print("[+] Creating results\' directory:", results_directory)
        os.makedirs(results_directory)

    results_filename = results_directory + cityname + "_" + category + ".json"
    print("[+] Saving file", results_filename)
    with open(results_filename, 'w') as fp:
        json.dump(dictionary, fp, indent=4)


def saveNDJSON(dictionary, cityname):

    if DEBUG:
        print("[+] Saving results in ndjson file")

    # create a directory if doesn't exists
    results_directory = "maps_me_results/"
    if not os.path.exists(results_directory):
        if DEBUG:
            print("[+] Creating results\' directory:", results_directory)
        os.makedirs(results_directory)

    results_filename = results_directory + cityname + ".json"
    print("[+] Saving file", results_filename)

    with open(results_filename, 'w', encoding='utf-8') as fp:
        poi_counter = 0
        for key, value in dictionary.items():
            fp.write('{"index":{"_id":'+str(poi_counter)+'}}\n')
            value_str = str(value).encode("utf-8")
            value_str = str(value_str).replace("\'", "\"")
            value_str = str(value_str)[2:-1]+"\n"
            fp.write(value_str)
            poi_counter += 1

def ingestdatatoelasticsearch(dictionary, cityname):
    from elasticsearch_functions import send_to_elasticsearch

    index_name = cityname + "-mapsme-dashboard"
    #index_name = "test-index"

    if DEBUG:
        print("[+] Ingesting results into elasticsearch - Index: " + index_name)

    send_to_elasticsearch(index_name, dictionary, '_doc')

def sendmessagetokafka(message, cityname):
    from kafka_functions import kafkasendmessage

    citynames = {"antalya": "ANT", "cork": "CRK", "antwerp": "ANW", "thessaloniki": "THE"}
    topic = "DATA_" + citynames[cityname] + "_ECO_MAPSME_CRAWLER"

    kafkasendmessage(topic, message)
