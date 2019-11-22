##This code is open-sourced software licensed under the MIT license
##Copyright 2019 Karypidis Paris - Alexandros, Democritus University of Thrace (DUTH)
##Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
##The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##
##DISCLAIMER
##This code is used to crawl/parse data from Eurostat databases. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.

"""
CUTLER H2020 Project
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
