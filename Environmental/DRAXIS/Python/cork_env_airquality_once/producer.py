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

This code is used to crawl/parse data from excel about Cork's air quality.
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import os
import json
import pandas as pd

from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *
from elastic import ElasticSearchClient

"""
The way this producer works is that it checks the number of docs in Elastic about the index "thess_env_airquality_daily"
If it isn't equal to 0 that means it's already populated with historical data. So broadcast only latest data
If it is 0, populates it with all historical data.

"""


def daily_aqi(pm10):
    """
    Function that uses an equation to compute daily AQI
    and returns a dict containing the value and
    the characterisation based on PM10 pollutant

    """
    if pm10 is None:
        return {
            "aqi_value": None,
            "aqi_characterisation": None
        }

    for bp_range in BREAKPOINTS_AQI.keys():
        bp_low = bp_range[0]
        bp_high = bp_range[1]
        if bp_low <= pm10 <= bp_high:
            i_low = BREAKPOINTS_AQI[bp_range]['i_low']
            i_high = BREAKPOINTS_AQI[bp_range]['i_high']

            aqi_value = ((i_high - i_low) / (bp_high - bp_low)) * (pm10 - bp_low) + i_low
            aqi_characterisation = BREAKPOINTS_AQI[bp_range]['characterisation']

            return {
                "aqi_value": aqi_value,
                "aqi_characterisation": aqi_characterisation
            }


def parse_excel(excel):

    df = pd.read_excel(excel, names=COLUMN_NAMES)

    # Replace nan values with None
    # to avoid errors later in ES mapping.
    df = df.where(pd.notnull(df), None)

    # replace empty string with None
    df = df.replace(' ', None)

    # group under pollutant, for Kibana-visualization reasons
    # df = pd.melt(df, id_vars=['Date'], var_name=['pollutant'])

    sent_messages = 0
    for index, row in df.iterrows():
        pm10 = row[2]
        aqi_res = daily_aqi(pm10)

        aqi_value = aqi_res['aqi_value']
        aqi_characterisation = aqi_res['aqi_characterisation']

        date = row.pop('Date')  # remove date
        date_iso = date.isoformat()

        location = {"lat": STATION_LAT, "lon": STATION_LON}
        station_name = STATION_NAME

        payload = {
            "Date": date_iso,
            "Pollutant": None,
            "Value": None,
            "aqi_value": aqi_value,
            "aqi_characterisation": aqi_characterisation,
            "location": location,
            "station_name": station_name
        }

        # now 'row' has only the pollutants to which we iterate
        for pollutant, value in row.iteritems():
            payload['Pollutant'] = pollutant
            payload['Value'] = value

            print(payload)
            producer.send(KAFKA_TOPIC, payload)
            sent_messages += 1

    print("Broadcasted total messages: {}".format(sent_messages))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

es = ElasticSearchClient(os.getenv('ES_HOST'), os.getenv('ES_PORT'),
                         use_ssl=os.getenv('ES_USE_SSL', False),
                         verify_certs=os.getenv('ES_VERIFY_CERTS', False),
                         http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')) if os.getenv('ES_USER') else None,
                         ca_certs=os.getenv('ES_CA_CERTS', None))

parse_excel(EXCEL_FILE)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
