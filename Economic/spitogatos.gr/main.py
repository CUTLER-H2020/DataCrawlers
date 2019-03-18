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
import os
from spitogatos import *
from categories import categories

if __name__ == "__main__":

    # use poi_counter to save all results in the same json file - avoid memory crashes
    poi_counter = 0
    if os.path.isfile('spitogatos_results/spitogatos.json'):
        os.remove('spitogatos_results/spitogatos.json')

    dictionary = downloadPOI("https://spitogatos.gr/search/results/residential/sale/r108/m108m109m110m/offset_", "Αγορά", "Κατοικία", "sale_residential_")
    poi_counter = saveNDJSON(dictionary, poi_counter)
    '''
    dictionary = downloadPOI("https://spitogatos.gr/search/results/commercial/sale/r108/m108m109m110m/offset_", "Αγορά", "Επαγγελματική στέγη", "sale_commercial_")
    poi_counter = saveNDJSON(dictionary, poi_counter)

    dictionary = downloadPOI("https://spitogatos.gr/search/results/land/sale/r108/m108m109m110m/offset_", "Αγορά", "Γη", "sale_land_")
    poi_counter = saveNDJSON(dictionary, poi_counter)

    dictionary = downloadPOI("https://spitogatos.gr/search/results/other/sale/r108/m108m109m110m/offset_", "Αγορά", "Λοιπά ακίνητα", "sale_other_")
    poi_counter = saveNDJSON(dictionary, poi_counter)


    dictionary = downloadPOI("https://spitogatos.gr/search/results/residential/rent/r108/m108m109m110m/offset_", "Ενοικίαση", "Κατοικία", "rent_residential_")
    poi_counter = saveNDJSON(dictionary, poi_counter)

    dictionary = downloadPOI("https://spitogatos.gr/search/results/commercial/rent/r108/m108m109m110m/offset_", "Ενοικίαση", "Επαγγελματική στέγη", "rent_commercial_")
    poi_counter = saveNDJSON(dictionary, poi_counter)

    dictionary = downloadPOI("https://spitogatos.gr/search/results/land/rent/r108/m108m109m110m/offset_", "Ενοικίαση", "Γη", "rent_other_")
    poi_counter = saveNDJSON(dictionary, poi_counter)

    dictionary = downloadPOI("https://spitogatos.gr/search/results/other/rent/r108/m108m109m110m/offset_", "Ενοικίαση", "Λοιπά ακίνητα", "rent_other_")
    poi_counter = saveNDJSON(dictionary, poi_counter)
    '''