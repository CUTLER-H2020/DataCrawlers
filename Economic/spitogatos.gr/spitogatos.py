
"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

headers - Dictionary with headers to be used in requests.get function
xpath_category - Dictionary with xpaths for every element scrapped from th url / every category use the same diction$

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
import os
import time
import json
import requests
import datetime
from lxml import html
from sources.sources import *


DEBUG = True

headers = {
    'User-Agent': 'Mozilla/5.0',  # required
}


xpath_category = {
    #  xpath to find result number
    "url_paggination": "//h2[@class='padding-left h5 searchTotalNumberOfResults']/b/text()",

    #  xpath to get title url - on every result page
    "xpath_poi_title_url": "//h4[@class='text color cyan larger  semibold searchListing_title']//@href",

    #xpath to get all property description
    "xpath_poi_desc_title": "//node()/div[contains(@class, 'desktop-3-details')]/h6/text()",
    "xpath_poi_desc_elements": "//node()/div[contains(@class, 'desktop-5-details')]//text()",
}


def downloadPOI(url_API, purpose, category, uniqueid_pattern):

    print("[+] Downloading data from spitogatos.gr:", (purpose, category, url_API))

    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month)

    # first find how many pages there are for this category
    try:
        page = requests.get(url_API, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        return False

    #  return how many results where found
    poi_pages = int(html.fromstring(page.text).xpath(xpath_category['url_paggination'])[0].replace(".", ""))
    print("[+] POIs found: " + str(poi_pages))
    page_counter = 0 #28790
    pois = {}
    poi_ascending_counter =  0
    while page_counter <= poi_pages:

        #time.sleep(5)  # comment this line to be more aggressive

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
            poi_desc_title = tree.xpath(xpath_category['xpath_poi_desc_title'])
#            print(len(poi_desc_title))
#            print(poi_desc_title)

            poi_desc_elements = tree.xpath(xpath_category['xpath_poi_desc_elements'])
            # replace all \n, \t, multiple space back and forth
            poi_desc_elements = [element.replace("\n", "").replace("\t", "").lstrip().rstrip() for element in poi_desc_elements]
            # remove all empty elements
            poi_desc_elements = list(filter(None, poi_desc_elements))
            # remove "price down" if it exists it should be in place 1-2
            if any("στις" in element for element in poi_desc_elements):  # works for now
                #print("DELETING...")
                del poi_desc_elements[1]
                del poi_desc_elements[1]
            #print(len(poi_desc_elements))
            #print(poi_desc_elements)

#            print(len(poi_desc_elements))
#            print(poi_desc_elements)

            poi = {}
            for i in range(len(poi_list_name)):
                if poi_list_name[i] in poi_desc_title:
                    # find poi_list_name index in poi_desc_title
                    element_index = poi_desc_title.index(poi_list_name[i])
                    #print(poi_list_name[i], poi_desc_elements[element_index])
                    poi[poi_list_name[i]] = poi_desc_elements[element_index].replace("€ ", "")
                else:
                    poi[poi_list_name[i]] = "0"
                poi["purpose"] = purpose
                poi["category"] = category
                poi["date"] = date
            pois[uniqueid_pattern + str(poi_ascending_counter)] = poi
            poi_ascending_counter += 1

            #break
        page_counter += 10
        #break

    if DEBUG:
        print("[+] Found:", len(pois))

    #save results in csv also
#    with open('spitogatos_results/' + uniqueid_pattern + '.csv', 'w', newline='', encoding='utf8') as f:
#        for key in pois.keys():
#            f.write("%s,%s\n" % (key, pois[key]))

    #for key, value in pois.items():
        #print(key, value)

    return pois


def saveNDJSON(dictionary, poi_counter):

    if DEBUG:
        print("[+] Saving results in ndjson file")

    # create a directory if doesn't exists
    results_directory = "spitogatos_results/"
    results_filename = results_directory + "spitogatos.json"
    if not os.path.exists(results_directory):
        if DEBUG:
            print("[+] Creating results\' directory:", results_directory)
        os.makedirs(results_directory)

    print("[+] Saving file", results_filename)
    with open(results_filename, 'a', encoding='utf8') as fp:
        for key, value in dictionary.items():
            fp.write('{"index":{"_id":'+str(poi_counter)+'}}\n')
            value_str = str(value)#.encode('utf-8')
            value_str = str(value_str).replace("\'", "\"") + "\n"
            fp.write(value_str)
            poi_counter += 1
    return poi_counter

def ingestdatatoelasticsearch(dictionary, index_name):
    from elasticsearch_functions import send_to_elasticsearch

    #index_name = "spitogatos-test"

    if DEBUG:
        print("[+] Ingesting results into elasticsearch - Index: " + index_name)

    send_to_elasticsearch(index_name, dictionary, '_doc')

def sendmessagetokafka(message, cityname):
    from kafka_functions import kafkasendmessage

    citynames = {"thessaloniki": "THE"}
    topic = "DATA_" + citynames[cityname] + "_ECO_SPITOGATOSGR_CRAWLER"

    kafkasendmessage(topic, message)

