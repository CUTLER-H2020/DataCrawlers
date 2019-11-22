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

The functions gets data in SDMX json format from eurostat url and create
a python dictionary with all the observations.
Then, each function returns its dictionary
"""
import os
import json
import urllib.request

# import operator

DEBUG = False

'''
Function to parse json data with 5 dimensions, 
eg. "unit","wstatus","nace_r2","geo","time"
'''


def parseeurostat5dimensions(url, dimensions):
    if DEBUG:
        print("[+] Reading json from url")
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    if DEBUG:
        print("[+] Reading data for: ", data['label'])

    # create the maps for the observations - what every digit means
    '''Within the json file, there is a 'dimension' element that contains the maps, though these maps are different 
    for every url. 
    eg. of maps
    "currency", "nace_r2", "geo","time"
    ID - how many combinations of ids exists, 
    eg. "id":["currency", "nace_r2", "geo","time"], "size":[3,2,4,2]
    observations are sorted based on ID
    '''
    firstdimMap = data['dimension'][dimensions[0]]['category']
    seconddimMap = data['dimension'][dimensions[1]]['category']
    thirddimMap = data['dimension'][dimensions[2]]['category']
    fourthdimMap = data['dimension'][dimensions[3]]['category']
    fifthdimMap = data['dimension'][dimensions[4]]['category']
    # idMap - See at 'Preparing observation maps' section

    # For every maps, create a python dictionary in order to create the unique ids for every observation
    if DEBUG:
        print("[+] Preparing observation maps")
    firstdim = {}  # should be in the order given in Map
    firstdimMapindex = firstdimMap['index']
    firstdimMaplabel = firstdimMap['label']
    for key, value in firstdimMapindex.items():
        firstdim[value] = {'id': key, 'label': firstdimMaplabel[key]}

    # for i, j in sorted(units.items(), key=operator.itemgetter(0)): #sorted by key
    #    print(i, j)

    seconddim = {}  # should be in the order given in Map
    seconddimMapindex = seconddimMap['index']
    seconddimMaplabel = seconddimMap['label']
    for key, value in seconddimMapindex.items():
        seconddim[value] = {'id': key, 'label': seconddimMaplabel[key]}

    thirddim = {}  # should be in the order given in Map
    thirddimMapindex = thirddimMap['index']
    thirddimMaplabel = thirddimMap['label']
    for key, value in thirddimMapindex.items():
        thirddim[value] = {'id': key, 'label': thirddimMaplabel[key]}

    fourthdim = {}  # should be in the order given in Map
    fourthdimMapindex = fourthdimMap['index']
    fourthdimMaplabel = fourthdimMap['label']
    for key, value in fourthdimMapindex.items():
        fourthdim[value] = {'id': key, 'label': fourthdimMaplabel[key]}

    fifthdim = {}  # should be in the order given in Map
    fifthdimMapindex = fifthdimMap['index']
    fifthdimMaplabel = fifthdimMap['label']
    for key, value in fifthdimMapindex.items():
        fifthdim[value] = {'id': key, 'label': fifthdimMaplabel[key]}

    ids = {}
    ids_counter = 0
    for index in range(len(data['id'])):
        ids[ids_counter] = {'id': data['id'][index], 'size': data['size'][index]}
        ids_counter += 1

    # For every observation, create a new entry in the 'observations' dictionary
    # dictionary with all eurostat observations
    # observationUnit, observationNa_item , observationGeo, observationTime, observationValue
    observations = {}

    if DEBUG:
        print("[+] Creating observation dictionary")

    # take all observations from json
    values = data['value']
    values = {int(k): float(v) for k, v in values.items()}  # cast keys in int to sort the dictionary

    observation_index = 0
    # index every observation based on 'unit' -> 'na_item' -> 'geo' -> 'time'
    for first in range(ids[0]['size']):
        for second in range(ids[1]['size']):
            for third in range(ids[2]['size']):
                for fourth in range(ids[3]['size']):
                    for fifth in range(ids[4]['size']):
                        # create a unique id for every observation
                        observationUniqueId = firstdim[first]['id'] + "-" + seconddim[second]['id'] \
                                              + "-" + thirddim[third]['id'] + "-" + fourthdim[fourth]['id'] \
                                              + "-" + fifthdim[fifth]['id']

                        # add the new observation as an element in observations dictionary
                        if observation_index in values:
                            observationValue = values[observation_index]
                            values.pop(observation_index, None)
                        else:
                            observationValue = "---"

                        observations[observationUniqueId] = {ids[0]['id']: firstdim[first]['label'],
                                                             ids[1]['id']: seconddim[second]['label'],
                                                             ids[2]['id']: thirddim[third]['label'],
                                                             ids[3]['id']: fourthdim[fourth]['label'],
                                                             ids[4]['id']: fifthdim[fifth]['label'],
                                                             'observationValue': observationValue}
                        observation_index += 1

    #    for i, j in sorted(observations.items(), key=operator.itemgetter(0)):  # sorted by key
    #        print(i, j)
    #        print("=================")
    if DEBUG:
        print("FOUND: " + str(len(observations)) + " observations")
        print(observations)
        print("===============\n")

    return observations


'''
Function to parse json data with 4 dimensions, 
eg. "currency", "nace_r2", "geo","time" or "unit", "na_item", "geo","time" 
'''


def parseeurostat4dimensions(url, dimensions):
    if DEBUG:
        print("[+] Reading json from url")
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    if DEBUG:
        print("[+] Reading data for: ", data['label'])

    # create the maps for the observations - what every digit means
    '''Within the json file, there is a 'dimension' element that contains the maps, though these maps are different 
    for every url. 
    eg. of maps
    "currency", "nace_r2", "geo","time"
    ID - how many combinations of ids exists, 
    eg. "id":["currency", "nace_r2", "geo","time"], "size":[3,2,4,2]
    observations are sorted based on ID
    '''
    firstdimMap = data['dimension'][dimensions[0]]['category']
    seconddimMap = data['dimension'][dimensions[1]]['category']
    thirddimMap = data['dimension'][dimensions[2]]['category']
    fourthdimMap = data['dimension'][dimensions[3]]['category']
    # idMap - See at 'Preparing observation maps' section

    # For every maps, create a python dictionary in order to create the unique ids for every observation
    if DEBUG:
        print("[+] Preparing observation maps")
    firstdim = {}  # should be in the order given in Map
    firstdimMapindex = firstdimMap['index']
    firstdimMaplabel = firstdimMap['label']
    for key, value in firstdimMapindex.items():
        firstdim[value] = {'id': key, 'label': firstdimMaplabel[key]}

    # for i, j in sorted(units.items(), key=operator.itemgetter(0)): #sorted by key
    #    print(i, j)

    seconddim = {}  # should be in the order given in Map
    seconddimMapindex = seconddimMap['index']
    seconddimMaplabel = seconddimMap['label']
    for key, value in seconddimMapindex.items():
        seconddim[value] = {'id': key, 'label': seconddimMaplabel[key]}

    thirddim = {}  # should be in the order given in Map
    thirddimMapindex = thirddimMap['index']
    thirddimMaplabel = thirddimMap['label']
    for key, value in thirddimMapindex.items():
        thirddim[value] = {'id': key, 'label': thirddimMaplabel[key]}

    fourthdim = {}  # should be in the order given in Map
    fourthdimMapindex = fourthdimMap['index']
    fourthdimMaplabel = fourthdimMap['label']
    for key, value in fourthdimMapindex.items():
        fourthdim[value] = {'id': key, 'label': fourthdimMaplabel[key]}

    ids = {}
    ids_counter = 0
    for index in range(len(data['id'])):
        ids[ids_counter] = {'id': data['id'][index], 'size': data['size'][index]}
        #        ids[data['id'][index]] = data['size'][index]
        ids_counter += 1
    # For every observation, create a new entry in the 'observations' dictionary
    # dictionary with all eurostat observations
    # observationUnit, observationNa_item , observationGeo, observationTime, observationValue
    observations = {}

    if DEBUG:
        print("[+] Creating observation dictionary")

    # take all observations from json
    values = data['value']
    values = {int(k): float(v) for k, v in values.items()}  # cast keys in int to sort the dictionary

    observation_index = 0
    # index every observation based on 'unit' -> 'na_item' -> 'geo' -> 'time'
    for first in range(ids[0]['size']):
        for second in range(ids[1]['size']):
            for third in range(ids[2]['size']):
                for fourth in range(ids[3]['size']):
                    # create a unique id for every observation
                    observationUniqueId = firstdim[first]['id'] + "-" + seconddim[second]['id'] \
                                          + "-" + thirddim[third]['id'] + "-" + fourthdim[fourth]['id']
                    # add the new observation as an element in observations dictionary
                    if observation_index in values:
                        observationValue = values[observation_index]
                        values.pop(observation_index, None)
                    else:
                        observationValue = "---"

                    observations[observationUniqueId] = {ids[0]['id']: firstdim[first]['label'],
                                                         ids[1]['id']: seconddim[second]['label'],
                                                         ids[2]['id']: thirddim[third]['label'],
                                                         ids[3]['id']: fourthdim[fourth]['label'],
                                                         'observationValue': observationValue}
                    observation_index += 1

    #    for i, j in sorted(observations.items(), key=operator.itemgetter(0)):  # sorted by key
    #        print(i, j)
    #        print("=================")
    if DEBUG:
        print("FOUND: " + str(len(observations)) + " observations")
        print(observations)
        print("===============\n")

    return observations


'''
Function to parse json data with 3 dimensions, 
eg. "unit","geo","time"
'''


def parseeurostat3dimensions(url, dimensions):
    if DEBUG:
        print("[+] Reading json from url")
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    if DEBUG:
        print("[+] Reading data for: ", data['label'])

    # create the maps for the observations - what every digit means
    '''Within the json file, there is a 'dimension' element that contains the maps, though these maps are different 
    for every url. 
    eg. of maps
    "unit","geo","time"
    ID - how many combinations of ids exists, 
    eg. "id":["unit","geo","time"], "size":[2,4,2]
    observations are sorted based on ID
    '''
    firstdimMap = data['dimension'][dimensions[0]]['category']
    seconddimMap = data['dimension'][dimensions[1]]['category']
    thirddimMap = data['dimension'][dimensions[2]]['category']
    # idMap - See at 'Preparing observation maps' section

    # For every maps, create a python dictionary in order to create the unique ids for every observation
    if DEBUG:
        print("[+] Preparing observation maps")
    firstdim = {}  # should be in the order given in Map
    firstdimMapindex = firstdimMap['index']
    firstdimMaplabel = firstdimMap['label']
    for key, value in firstdimMapindex.items():
        firstdim[value] = {'id': key, 'label': firstdimMaplabel[key]}

    # for i, j in sorted(units.items(), key=operator.itemgetter(0)): #sorted by key
    #    print(i, j)

    seconddim = {}  # should be in the order given in Map
    seconddimMapindex = seconddimMap['index']
    seconddimMaplabel = seconddimMap['label']
    for key, value in seconddimMapindex.items():
        seconddim[value] = {'id': key, 'label': seconddimMaplabel[key]}

    thirddim = {}  # should be in the order given in Map
    thirddimMapindex = thirddimMap['index']
    thirddimMaplabel = thirddimMap['label']
    for key, value in thirddimMapindex.items():
        thirddim[value] = {'id': key, 'label': thirddimMaplabel[key]}

    ids = {}
    ids_counter = 0
    for index in range(len(data['id'])):
        ids[ids_counter] = {'id': data['id'][index], 'size': data['size'][index]}
        #        ids[data['id'][index]] = data['size'][index]
        ids_counter += 1

    # For every observation, create a new entry in the 'observations' dictionary
    # dictionary with all eurostat observations
    # observationUnit, observationNa_item , observationGeo, observationTime, observationValue
    observations = {}

    if DEBUG:
        print("[+] Creating observation dictionary")

    # take all observations from json
    values = data['value']
    values = {int(k): float(v) for k, v in values.items()}  # cast keys in int to sort the dictionary

    observation_index = 0
    # index every observation based on 'unit' -> 'na_item' -> 'geo' -> 'time'
    for first in range(ids[0]['size']):
        for second in range(ids[1]['size']):
            for third in range(ids[2]['size']):
                # create a unique id for every observation
                observationUniqueId = firstdim[first]['id'] + "-" + seconddim[second]['id'] \
                                      + "-" + thirddim[third]['id']

                # add the new observation as an element in observations dictionary
                if observation_index in values:
                    observationValue = values[observation_index]
                    values.pop(observation_index, None)
                else:
                    observationValue = "---"

                observations[observationUniqueId] = {ids[0]['id']: firstdim[first]['label'],
                                                     ids[1]['id']: seconddim[second]['label'],
                                                     ids[2]['id']: thirddim[third]['label'],
                                                     'observationValue': observationValue}

                observation_index += 1

        # for i, j in sorted(observations.items(), key=operator.itemgetter(0)):  # sorted by key
        #    print(i, j)
        #    print("=================")

    if DEBUG:
        print("FOUND: " + str(len(observations)) + " observations")
        print(observations)
        print("===============\n")

    return observations


def saveJSON(dataset, dataset_name):
    if DEBUG:
        print("[+] Saving dataset in json file")

    # create a directory if doesn't exists
    results_directory = "eurostat_results/"
    if not os.path.exists(results_directory):
        if DEBUG:
            print("[+] Creating results\' directory:", results_directory)
        os.makedirs(results_directory)

    results_filename = results_directory + dataset_name + ".json"
    print("[+] Saving file", results_filename)
    with open(results_filename, 'w') as fp:
        json.dump(dataset, fp, indent=4)
