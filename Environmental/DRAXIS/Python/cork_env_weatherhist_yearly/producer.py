import os
import json
import requests
import time
import math
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *

"""
The way this crawler (and similarly the other 2) works to get data from DRAXIS' Climatology API
is the following.

For every climatology index (4 in total - temp-avg, wind, rh, total-prec) we issue a request
to get the path of the dataset, inside a THREDDS server that contains the netCDF file with the data.

However due to intense processing in the backround, the API when for example you ask the first time 
to get the dataset it may return {status: processing} until it process all the data and after it's ready 
it returns {status: ready}

From the response we need 2 things.
    - the path of the dataset
    - the variable name of the index (which in some cases is different that the one referenced in the constants module)

Specifically the names of the variables of each index we get back from each request are:
   - temp-avg --> t2m
   - wind --> u10 AND v10 (2 variables)
   - rh --> rh
   - total-prec --> tp

Then after we have the path of the dataset and the variable name
we issue another request to another endpoint, 
providing these two information (the path of the dataset is part of the URL, and the variable as a parameter)
to get back the timeseries data.

(Wind is a special case where we have 2 variables (u10, v10) and hence 2 timeseries data that are not returned 
in the dataset request. The final result is the combination of these two by 
using the hypotenuse of each value for every date point)

Finally we broadcast the data through Kafka, we consume them and inserting them to Elasticsearch
"""


def __issue_request(path_dataset, variable):
    params = {
        'lat': CORK_LAT,
        'lon': CORK_LON,
        'variable': variable,
        'from_date': STARTING_DATE,
        'apikey': os.getenv("API_KEY")
    }

    url = "{}/data/timeseries/{}".format(os.getenv("DRAXIS_API_CLIMATOLOGY_URL"),
                                         path_dataset)

    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Error issuing request to DRAXIS Climatology API at: {} with params: {}".
              format(url, params))
        raise ClimatologyException

    res = response.json()

    return res


def get_timeseries_data(index):
    dataset = _get_dataset(index)

    def _get_wind_timeseries_data():
        path_dataset = dataset['dataset_path']

        timeseries_data_u10 = __issue_request(path_dataset, WIND_X_AXIS_VARIABLE)
        timeseries_data_v10 = __issue_request(path_dataset, WIND_Y_AXIS_VARIABLE)

        interpolated_timeseries = {}

        for date, value_u10 in timeseries_data_u10.items():
            try:
                value_v10 = timeseries_data_v10.get(date)

                interpolated_value = math.hypot(value_u10, value_v10)
                interpolated_timeseries[date] = interpolated_value

            except ClimatologyException as e:
                print("Can't apply interpolation between the 2 wind datasets. Unmatched dates!")
                raise ClimatologyException

        return interpolated_timeseries

    if index == 'wind':
        return _get_wind_timeseries_data()

    path_dataset = dataset['dataset_path']
    variable = dataset['index_variable']

    return __issue_request(path_dataset, variable)


def _get_dataset(index):
    while True:
        params = {
            'bbox': BBOX_CSV,
            'apikey': os.getenv("API_KEY"),
            'from_date': STARTING_DATE
        }

        url = "{}/indices/era5/{}".format(os.getenv("DRAXIS_API_CLIMATOLOGY_URL"),
                                          index)
        response = requests.get(url=url, params=params)
        res = response.json()
        print(res['status'])

        if res['status'] == 'ready':
            break

        time.sleep(10)

    dataset_path = res['results'][0]['path']
    index_variable = res['results'][0]['variable']

    return {'dataset_path': dataset_path, 'index_variable': index_variable}


def broadcast_data(climatology_index, metadata):
    values = get_timeseries_data(climatology_index)

    payload = {
        'location': {'lat': CORK_LAT, 'lon': CORK_LON},
        'Variable': climatology_index,
        'Description': metadata['description'],
        'Unit': metadata['unit']
    }

    for date, value in values.items():
        # for Kibana visualisation reasons, cut values below 0.001
        if -0.001 < value < 0.001:
            value = 0.0

        payload['Date'] = date
        payload['Value'] = value

        print(payload)
        producer.send(KAFKA_TOPIC, payload)


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

for climatology_index, metadata in INDEX_METADATA_MAPPING.items():
    broadcast_data(climatology_index=climatology_index, metadata=metadata)


# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
