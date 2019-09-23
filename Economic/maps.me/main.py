"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

The script downloads data for five basic categories and specific cities from maps.me
Categories: Lodging, Shops, Food, Entertainment, Attraction (see sources/ directory)
Cities: Thessaloniki - Greece, Cork - Ireland, TBC (see cities.py)
"""
import datetime
from mapsme import *
from cities import cities
from sources.lodging import *
from sources.shops import *
from sources.food import *
from sources.entertainment import *
from sources.attractions import *

if __name__ == "__main__":

    for cityname, country_locality in cities.items():
        #  Download Lodging Category
        print("[+] Downloading data for Town:", cityname)
        dictionary = downloadPOI(xpaths_hotel, country_locality)
        dictionary.update(downloadPOI(xpaths_guest_houses, country_locality))
        '''
        dictionary.update(downloadPOI(xpaths_motels, country_locality))
        dictionary.update(downloadPOI(xpaths_camping, country_locality))
        dictionary.update(downloadPOI(xpaths_hostels, country_locality))
        dictionary.update(downloadPOI(xpaths_apartments, country_locality))
        print("[+] Done for lodging category")
        print("=====================\n")

        #  Download Shops Category
        dictionary.update(downloadPOI(xpaths_supermarkets, country_locality))
        dictionary.update(downloadPOI(xpaths_clothes, country_locality))
        dictionary.update(downloadPOI(xpaths_mall, country_locality))
        dictionary.update(downloadPOI(xpaths_marketplace, country_locality))
        dictionary.update(downloadPOI(xpaths_hardware, country_locality))
        dictionary.update(downloadPOI(xpaths_furniture, country_locality))
        dictionary.update(downloadPOI(xpaths_alcohol, country_locality))
        dictionary.update(downloadPOI(xpaths_shoes, country_locality))
        dictionary.update(downloadPOI(xpaths_department_store, country_locality))
        dictionary.update(downloadPOI(xpaths_sports, country_locality))
        dictionary.update(downloadPOI(xpaths_bakery, country_locality))
        dictionary.update(downloadPOI(xpaths_computer, country_locality))
        dictionary.update(downloadPOI(xpaths_jewelry, country_locality))
        dictionary.update(downloadPOI(xpaths_books, country_locality))
        dictionary.update(downloadPOI(xpaths_beauty, country_locality))
        dictionary.update(downloadPOI(xpaths_butcher, country_locality))
        dictionary.update(downloadPOI(xpaths_toys, country_locality))
        dictionary.update(downloadPOI(xpaths_florist, country_locality))
        dictionary.update(downloadPOI(xpaths_gift, country_locality))
        dictionary.update(downloadPOI(xpaths_ticket, country_locality))
        dictionary.update(downloadPOI(xpaths_confectionery, country_locality))
        dictionary.update(downloadPOI(xpaths_kiosk, country_locality))
        dictionary.update(downloadPOI(xpaths_wine, country_locality))
        dictionary.update(downloadPOI(xpaths_photo, country_locality))
        dictionary.update(downloadPOI(xpaths_chemist, country_locality))
        print("[+] Done for shop category")
        print("=====================\n")

        #  Download Food Category
        dictionary.update(downloadPOI(xpaths_restaurant, country_locality))
        dictionary.update(downloadPOI(xpaths_cafe, country_locality))
        dictionary.update(downloadPOI(xpaths_fast_food, country_locality))
        dictionary.update(downloadPOI(xpaths_bar, country_locality))
        dictionary.update(downloadPOI(xpaths_pub, country_locality))
        print("[+] Done for food category")
        print("=====================\n")

        #  Download Entertainment Category
        dictionary.update(downloadPOI(xpaths_park, country_locality))
        dictionary.update(downloadPOI(xpaths_sauna, country_locality))
        dictionary.update(downloadPOI(xpaths_nightclub, country_locality))
        dictionary.update(downloadPOI(xpaths_cinema, country_locality))
        dictionary.update(downloadPOI(xpaths_stadium, country_locality))
        dictionary.update(downloadPOI(xpaths_library, country_locality))
        dictionary.update(downloadPOI(xpaths_casino, country_locality))
        dictionary.update(downloadPOI(xpaths_fitness_center, country_locality))
        dictionary.update(downloadPOI(xpaths_swimming_pool, country_locality))
        dictionary.update(downloadPOI(xpaths_theater, country_locality))
        dictionary.update(downloadPOI(xpaths_water_park, country_locality))
        dictionary.update(downloadPOI(xpaths_zoo, country_locality))
        dictionary.update(downloadPOI(xpaths_man_made_pier, country_locality))
        dictionary.update(downloadPOI(xpaths_multi, country_locality))
        dictionary.update(downloadPOI(xpaths_football, country_locality))
        dictionary.update(downloadPOI(xpaths_basketball, country_locality))
        dictionary.update(downloadPOI(xpaths_athletics, country_locality))
        print("[+] Done for entertainment category")
        print("=====================\n")

        #  Download Attractions Category
        dictionary.update(downloadPOI(xpaths_place_of_worship_christian, country_locality))
        dictionary.update(downloadPOI(xpaths_attraction, country_locality))
        dictionary.update(downloadPOI(xpaths_place_of_worship_muslim, country_locality))
        dictionary.update(downloadPOI(xpaths_viewpoint, country_locality))
        dictionary.update(downloadPOI(xpaths_museum, country_locality))
        dictionary.update(downloadPOI(xpaths_castle, country_locality))
        dictionary.update(downloadPOI(xpaths_monument, country_locality))
        dictionary.update(downloadPOI(xpaths_memorial, country_locality))
        dictionary.update(downloadPOI(xpaths_place_of_worship_jewish, country_locality))
        dictionary.update(downloadPOI(xpaths_tomb, country_locality))
        dictionary.update(downloadPOI(xpaths_wayside_shrine, country_locality))
        dictionary.update(downloadPOI(xpaths_place_of_worship_taoist, country_locality))
        print("[+] Done, for attractions category")
        print("=====================\n[+] Done!")
        '''

        citynames = {"Antalya - Turkey": "ANT", "Cork - Ireland": "CRK", "Antwerp - Belgium": "ANW", "Thessaloniki - Greece": "THE"}
        download_topic = "DATA_DOWNLOAD_" + citynames[cityname] + "_ECO_MAPSME_CRAWLER"
        ingest_topic = "DATA_INGESTION_" + citynames[cityname] + "_ECO_MAPSME_CRAWLER"

        # save them in NDjson based on "cityname"
        saveNDJSON(dictionary, cityname)
        sendmessagetokafka("Data for " + cityname + " were downloaded successfully - Data cat be found in maps_me_results/" + cityname + ".json file - Date: " + str(datetime.date.today()), download_topic)

        cityname = (cityname.split(" ")[0]).lower()
        ingestdatatoelasticsearch(dictionary, cityname)
        sendmessagetokafka("Data for " + cityname + " were ingested successfully - Data cat be found in " + cityname + "-mapsme-dashboard elasticsearch index - Date: " + str(datetime.date.today()), ingest_topic)

