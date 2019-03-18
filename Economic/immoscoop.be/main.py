"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

The script downloads data for five basic categories and specific cities from maps.me and saves in several json files
Categories: Lodging, Shops, Food, Entertainment, Attraction (see sources/ directory)
Cities: Thessaloniki - Greece, Cork - Ireland, TBC (see categories.py)
Results: the script creates a directory (if not exists), an saves the data based on city and category
"""
from immoscoop import *

if __name__ == "__main__":

    # use poi_counter to save all results in the same json file - avoid memory crashes
    poi_counter = 0
    if os.path.isfile('immoscoop_results/immoscoop.json'):
        os.remove('immoscoop_results/immoscoop.json')


    dictionary = downloadPOI(
        "https://www.immoscoop.be/eng/immo.php?search_field=&main_city%5B%5D=2421&s_postcode%5B%5D=56&s_postcode%5B%5D=57&s_postcode%5B%5D=58&s_postcode%5B%5D=59&s_postcode%5B%5D=2420&s_postcode%5B%5D=1546&s_postcode%5B%5D=160&s_postcode%5B%5D=910&s_postcode%5B%5D=61&s_postcode%5B%5D=62&s_postcode%5B%5D=371&s_postcode%5B%5D=231&s_postcode%5B%5D=994&s_postcode%5B%5D=422&s_postcode%5B%5D=158&s_postcode%5B%5D=1521&s_postcode%5B%5D=703&category=&min_price=0&max_price=&bedroom=&baths=&order=city&proptype=Sale&page=",
        "Sale", "sale_")
    poi_counter = saveNDJSON(dictionary, poi_counter)

#    dictionary = downloadPOI(
#        "https://www.immoscoop.be/eng/immo.php?search_field=&main_city%5B%5D=2421&s_postcode%5B%5D=56&s_postcode%5B%5D=57&s_postcode%5B%5D=58&s_postcode%5B%5D=59&s_postcode%5B%5D=2420&s_postcode%5B%5D=1546&s_postcode%5B%5D=160&s_postcode%5B%5D=910&s_postcode%5B%5D=61&s_postcode%5B%5D=62&s_postcode%5B%5D=371&s_postcode%5B%5D=231&s_postcode%5B%5D=994&s_postcode%5B%5D=422&s_postcode%5B%5D=158&s_postcode%5B%5D=1521&s_postcode%5B%5D=703&category=&min_price=0&max_price=&bedroom=&baths=&order=city&proptype=Rent&page=",
#        "Rent", "rent_")
#    poi_counter = saveNDJSON(dictionary, poi_counter)
