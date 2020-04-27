"""
This code is open-sourced software licensed under the MIT license. (http://opensource.org/licenses/MIT)

Copyright 2020 Stergios Bampakis, DRAXIS ENVIRONMENTAL S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

DISCLAIMER

This code is used to crawl/parse data from Cork's Archive Water Level API (http://waterlevel.ie/hydro-data/home.html)
for Ballea and Ringaskiddy NMCI stations.
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import os
import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *

"""
Producer that downloads historical data for each of the stations and broadcast them
in the Kafka topic

"""

HISTORICAL_DATA_BASE_URL = "http://waterlevel.ie/hydro-data/stations/{}/Parameter/S/complete.zip"

DAILY_BASE_URL = "http://waterlevel.ie/data"
WATER_QUALITY_CODE = 0o001  # literal int: 0001


def broadcast_historical_data(station, station_id):
    url = HISTORICAL_DATA_BASE_URL.format(station_id)

    # This url downloads the file as a zip. Pandas handle downloading and decompression on-the-fly
    # Skip the first 6 rows that contain info and
    # use only first and second row with date and values (quality is not a requirement)
    df = pd.read_csv(url, sep='\t', compression='zip', header=6, usecols=[0, 1])

    # convert dates from string to datetime object for easy extraction of it's parts
    df['Date'] = pd.to_datetime(df['Date'])

    # Replace nan values with None
    # to avoid errors later in ES mapping.
    df = df.where(pd.notnull(df), None)

    # for the Ballea case, historical data start from 1972 until 2020. Those are really big data
    # and takes incredible much time to process them one by one. Since we don't need all of them
    # we will discard the dates before 2012-01-01 and keep only those that are past to it
    threshold = datetime.datetime(2012, 1, 1)
    df = df[df['Date'] >= threshold]

    # The following attributes apply to all rows in csv
    payload = {
        'location': {'lat': STATIONS_LOCATION.get(station)[0], 'lon': STATIONS_LOCATION.get(station)[1]},
        'station_name': station,
        'unit': 'm'
    }

    for row in df.itertuples():
        date_obj = row.Date
        water_level = row.Value

        # populate the payload with the rest of the parts of each row
        payload['date'] = date_obj.isoformat()

        payload['day'] = date_obj.day
        payload['month'] = date_obj.month
        payload['year'] = date_obj.year

        payload['hour'] = date_obj.time().isoformat()

        payload['water_level'] = water_level

        # send payload to producer
        producer.send(KAFKA_TOPIC, payload)


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))


for station_name, station_id in STATIONS_ID.items():
    broadcast_historical_data(station_name, station_id)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
