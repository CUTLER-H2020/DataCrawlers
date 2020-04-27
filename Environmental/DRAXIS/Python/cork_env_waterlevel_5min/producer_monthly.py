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

This code is used to crawl/parse data from Cork's Realtime Water Level API (http://waterlevel.ie/page/api/).
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
from elastic import ElasticSearchClient

MONTHLY_BASE_URL = "http://waterlevel.ie/data"
WATER_QUALITY_CODE = 0o001  # literal int: 0001


def broadcast_monthly_data(station):
    url = "{}/month/{}_{:04d}.csv".format(MONTHLY_BASE_URL, STATIONS_ID.get(station), WATER_QUALITY_CODE)

    # No need to download the csv files !
    # Pandas can handle this on-the-fly
    df = pd.read_csv(url)

    # convert dates from string to datetime object for easy extraction of it's parts
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Replace nan values with None
    # to avoid errors later in ES mapping.
    df = df.where(pd.notnull(df), None)

    # The following attributes apply to all rows in csv
    payload = {
        'location': {'lat': STATIONS_LOCATION.get(station)[0], 'lon': STATIONS_LOCATION.get(station)[1]},
        'station_name': station,
        'unit': 'm'
    }
    print(url)

    for row in df.itertuples():
        date_obj = row.datetime
        water_level = row.value

        # populate the payload with the rest of the parts of each row
        payload['date'] = date_obj.isoformat()

        payload['day'] = date_obj.day
        payload['month'] = date_obj.month
        payload['year'] = date_obj.year

        payload['hour'] = date_obj.time().isoformat()

        payload['water_level'] = water_level

        print(payload)
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
    broadcast_monthly_data(station_name)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
