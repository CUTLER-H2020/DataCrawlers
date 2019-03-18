"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

The script downloads data for five basic categories and specific cities from maps.me and saves in several json files
Categories: Lodging, Shops, Food, Entertainment, Attraction (see sources/ directory)
Cities: Thessaloniki - Greece, Cork - Ireland, TBC (see cities.py)
Results: the script creates a directory (if not exists), an saves the data based on city and category
"""
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
        dictionary.update(downloadPOI(xpaths_motels, country_locality))
        dictionary.update(downloadPOI(xpaths_camping, country_locality))
        dictionary.update(downloadPOI(xpaths_hostels, country_locality))
        dictionary.update(downloadPOI(xpaths_apartments, country_locality))
        # save them in json a json file based on "country_locality" and "category"
#        saveJSON(lodging, cityname, "lodging")
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
        # save them in json a json file based on "country_locality" and "category"
#        saveJSON(shops, cityname, "shop")
        print("[+] Done for shop category")
        print("=====================\n")

        #  Download Food Category
        dictionary.update(downloadPOI(xpaths_restaurant, country_locality))
        dictionary.update(downloadPOI(xpaths_cafe, country_locality))
        dictionary.update(downloadPOI(xpaths_fast_food, country_locality))
        dictionary.update(downloadPOI(xpaths_bar, country_locality))
        dictionary.update(downloadPOI(xpaths_pub, country_locality))
        # save them in json a json file based on "country_locality" and "category"
#        saveJSON(food, cityname, "food")
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
        # save them in json a json file based on "country_locality" and "category"
#        saveJSON(entertainment, cityname, "entertainment")
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
        # save them in json a json file based on "country_locality" and "category"
#        saveJSON(attractions, cityname, "attractions")
        print("[+] Done, for attractions category")
        print("=====================\n[+] Done!")

        saveNDJSON(dictionary, cityname)


        '''
        #  Download Lodging Category
        print("[+] Downloading data for Town:", cityname)
        lodging = downloadPOI(xpaths_hotel, country_locality)
        lodging.update(downloadPOI(xpaths_guest_houses, country_locality))
        lodging.update(downloadPOI(xpaths_motels, country_locality))
        lodging.update(downloadPOI(xpaths_camping, country_locality))
        lodging.update(downloadPOI(xpaths_hostels, country_locality))
        lodging.update(downloadPOI(xpaths_apartments, country_locality))
        #save them in json a json file based on "country_locality" and "category"
        saveJSON(lodging, cityname, "lodging")
        print("[+] For lodging category - Found:", len(lodging))
        print("=====================\n")

        #  Download Shops Category
        shops = downloadPOI(xpaths_supermarkets, country_locality)
        shops.update(downloadPOI(xpaths_clothes, country_locality))
        shops.update(downloadPOI(xpaths_mall, country_locality))
        shops.update(downloadPOI(xpaths_marketplace, country_locality))
        shops.update(downloadPOI(xpaths_hardware, country_locality))
        shops.update(downloadPOI(xpaths_furniture, country_locality))
        shops.update(downloadPOI(xpaths_alcohol, country_locality))
        shops.update(downloadPOI(xpaths_shoes, country_locality))
        shops.update(downloadPOI(xpaths_department_store, country_locality))
        shops.update(downloadPOI(xpaths_sports, country_locality))
        shops.update(downloadPOI(xpaths_bakery, country_locality))
        shops.update(downloadPOI(xpaths_computer, country_locality))
        shops.update(downloadPOI(xpaths_jewelry, country_locality))
        shops.update(downloadPOI(xpaths_books, country_locality))
        shops.update(downloadPOI(xpaths_beauty, country_locality))
        shops.update(downloadPOI(xpaths_butcher, country_locality))
        shops.update(downloadPOI(xpaths_toys, country_locality))
        shops.update(downloadPOI(xpaths_florist, country_locality))
        shops.update(downloadPOI(xpaths_gift, country_locality))
        shops.update(downloadPOI(xpaths_ticket, country_locality))
        shops.update(downloadPOI(xpaths_confectionery, country_locality))
        shops.update(downloadPOI(xpaths_kiosk, country_locality))
        shops.update(downloadPOI(xpaths_wine, country_locality))
        shops.update(downloadPOI(xpaths_photo, country_locality))
        shops.update(downloadPOI(xpaths_chemist, country_locality))
        #save them in json a json file based on "country_locality" and "category"
        saveJSON(shops, cityname, "shop")
        print("[+] For shop category - Found:", len(shops))
        print("=====================\n")
        
        #  Download Food Category
        food = downloadPOI(xpaths_restaurant, country_locality)
        food.update(downloadPOI(xpaths_cafe, country_locality))
        food.update(downloadPOI(xpaths_fast_food, country_locality))
        food.update(downloadPOI(xpaths_bar, country_locality))
        food.update(downloadPOI(xpaths_pub, country_locality))
        #save them in json a json file based on "country_locality" and "category"
        saveJSON(food, cityname, "food")
        print("[+] For food category - Found:", len(food))
        print("=====================\n")
        
        #  Download Entertainment Category
        entertainment = downloadPOI(xpaths_park, country_locality)
        entertainment.update(downloadPOI(xpaths_sauna, country_locality))
        entertainment.update(downloadPOI(xpaths_nightclub, country_locality))
        entertainment.update(downloadPOI(xpaths_cinema, country_locality))
        entertainment.update(downloadPOI(xpaths_stadium, country_locality))
        entertainment.update(downloadPOI(xpaths_library, country_locality))
        entertainment.update(downloadPOI(xpaths_casino, country_locality))
        entertainment.update(downloadPOI(xpaths_fitness_center, country_locality))
        entertainment.update(downloadPOI(xpaths_swimming_pool, country_locality))
        entertainment.update(downloadPOI(xpaths_theater, country_locality))
        entertainment.update(downloadPOI(xpaths_water_park, country_locality))
        entertainment.update(downloadPOI(xpaths_zoo, country_locality))
        entertainment.update(downloadPOI(xpaths_man_made_pier, country_locality))
        entertainment.update(downloadPOI(xpaths_multi, country_locality))
        entertainment.update(downloadPOI(xpaths_football, country_locality))
        entertainment.update(downloadPOI(xpaths_basketball, country_locality))
        entertainment.update(downloadPOI(xpaths_athletics, country_locality))
        #save them in json a json file based on "country_locality" and "category"
        saveJSON(entertainment, cityname, "entertainment")
        print("[+] For entertainment category - Found:", len(entertainment))
        print("=====================\n")

        #  Download Attractions Category
        attractions = downloadPOI(xpaths_place_of_worship_christian, country_locality)
        attractions.update(downloadPOI(xpaths_attraction, country_locality))
        attractions.update(downloadPOI(xpaths_place_of_worship_muslim, country_locality))
        attractions.update(downloadPOI(xpaths_viewpoint, country_locality))
        attractions.update(downloadPOI(xpaths_museum, country_locality))
        attractions.update(downloadPOI(xpaths_castle, country_locality))
        attractions.update(downloadPOI(xpaths_monument, country_locality))
        attractions.update(downloadPOI(xpaths_memorial, country_locality))
        attractions.update(downloadPOI(xpaths_place_of_worship_jewish, country_locality))
        attractions.update(downloadPOI(xpaths_tomb, country_locality))
        attractions.update(downloadPOI(xpaths_wayside_shrine, country_locality))
        attractions.update(downloadPOI(xpaths_place_of_worship_taoist, country_locality))
        #save them in json a json file based on "country_locality" and "category"
        saveJSON(attractions, cityname, "attractions")
        print("[+] For attractions category - Found:", len(attractions))
        print("=====================\n[+] Done!")
        '''