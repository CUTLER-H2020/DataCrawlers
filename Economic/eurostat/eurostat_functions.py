"""
Written by Karypidis Paris Alexandros
Democritus University of Thrace (DUTH)
2018 within CUTLER H2020 Project
Python 3.5

The functions gets data in SDMX json format from eurostat url and create
a python dictionary with all the observations.
Then, each function returns its dictionary
"""

import urllib.request
import json
import operator

DEBUG = False

'''
Function to parse json data with 5 dimensions, 
eg. "unit","wstatus","nace_r2","geo","time"
'''


def parseeurostat5dimensions(url, firstdim, seconddim, thirddim, fourthdim, fifthdim):
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
    firstdimMap = data['dimension'][firstdim]['category']
    seconddimMap = data['dimension'][seconddim]['category']
    thirddimMap = data['dimension'][thirddim]['category']
    fourthdimMap = data['dimension'][fourthdim]['category']
    fifthdimMap = data['dimension'][fifthdim]['category']
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


def parseeurostat4dimensions(url, firstdim, seconddim, thirddim, fourthdim):
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
    firstdimMap = data['dimension'][firstdim]['category']
    seconddimMap = data['dimension'][seconddim]['category']
    thirddimMap = data['dimension'][thirddim]['category']
    fourthdimMap = data['dimension'][fourthdim]['category']
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


def parseeurostat3dimensions(url, firstdim, seconddim, thirddim):
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
    firstdimMap = data['dimension'][firstdim]['category']
    seconddimMap = data['dimension'][seconddim]['category']
    thirddimMap = data['dimension'][thirddim]['category']
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

    #    for i, j in sorted(observations.items(), key=operator.itemgetter(0)):  # sorted by key
    #        print(i, j)
    #        print("=================")

    if DEBUG:
        print("FOUND: " + str(len(observations)) + " observations")
        print(observations)
        print("===============\n")

    return observations


'''
#Save every obseravtion to a csv file based on its Metropolitan Area
#Columns -> Obseravtion Year
#Rows -> Obseravtion Variables
#	
import csv
import os

#create a directory if doesn't exists
results_directory = "oecd_metropolitan_areas_results/"
if not os.path.exists(results_directory):
    print("[+] Creating results\' directory")
    os.makedirs(results_directory)


#Create unique ids to extracts observations from python dictionary
#for every Metropolitan Area
for locations_name, locations_id in sorted(locations.items(), key=operator.itemgetter(1)):

    csvfilename = str(results_directory) + str(locations_name) + ".csv"
    print("[+] Saving dictionary to csv files: " + csvfilename)
    print("[+] Saving csv files: " + csvfilename)

    with open(csvfilename, 'w', newline='', encoding="utf8") as csvfile:
        wr = csv.writer(csvfile)

        #write headers in csv file
        #Name of Metropolitan Area
        #'Variable', years (min -> max)
        wr.writerow(["Metropolitan Area: " + locations_name])
        yearsforcsv = [key for key, val in sorted(years.items(), key=operator.itemgetter(1))]
        wr.writerow(["Variables/Years"] + yearsforcsv)

        #for every variable
        for variable_name, variable_id in sorted(variables.items(), key=operator.itemgetter(1)):
            #for every year
            observationList = [] #create a temporary list to save each csv row
            for year_name, year_id in sorted(years.items(), key=operator.itemgetter(1)):
                search_unique_id = locations_id + variable_id + year_id
                if DEBUG:
                    print(locations_name + "-" + variable_name + "-" + year_name + " : " + search_unique_id)

                #create a list with all years' variables                    
                if search_unique_id in observations:
                    observationList.append(observations[search_unique_id]['observationValue'])
                    #pop element for speed
                    observations.pop(search_unique_id, None)
                else:
                    observationList.append("---")

            wr.writerow([variable_name] + observationList)
print("[+] Finish")
'''
