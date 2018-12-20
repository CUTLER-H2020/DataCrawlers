"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

The main functions gets data in SDMX json format from selected eurostat urls and saves them in JSON files
"""
import time
from eurostat_functions import *
from sources import *

if __name__ == "__main__":
    print("[+] Downloading data from Eurostat")

    datasets = [demo_r_d3dens, demo_r_pjanind3, nama_10r_3popgdp, nama_10r_3gdp, nama_10r_3gva, nama_10r_3empers,
                nama_10r_2hhinc, nama_10r_2hhsec, tour_cap_nuts3, met_10r_3emp, met_10r_3gdp, met_lfp3pop, urb_cecfi,
                urb_ctour]

    for dataset in datasets:
        print("[+] Eurostat -", dataset['name'])
        if dataset['dimension_count'] == 3:
            dataset_dict = parseeurostat3dimensions(dataset['url'], dataset['dimensions'])
        elif dataset['dimension_count'] == 4:
            dataset_dict = parseeurostat4dimensions(dataset['url'], dataset['dimensions'])
        else:
            dataset_dict = parseeurostat5dimensions(dataset['url'], dataset['dimensions'])

        print("[+] Found: " + str(len(dataset_dict)) + " observations")
        # call saveJSON(dataset dictionary, dataset name)
        saveJSON(dataset_dict, dataset['name'])
