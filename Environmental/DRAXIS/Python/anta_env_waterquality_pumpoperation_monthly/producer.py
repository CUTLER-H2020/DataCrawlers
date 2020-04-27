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

This code is used to crawl/parse data from file from Antalya Municipality (antalya_all_data.xlsx).
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


def parse_file(excel):
    df = pd.read_excel(excel, usecols=[0, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33])

    df = pd.melt(df,
                 id_vars=["Date",
                          "MONTH",
                          "kw/hour",
                          "Waterflow(BeforePump)",
                          "Waterflow(AfterPump)"],
                 var_name='Parameter',
                 value_name='Value')

    # Replace nan values with None
    # to avoid errors later in ES mapping.
    df = df.where(pd.notnull(df), None)

    # Rename column 'MONTH' to 'month'
    df = df.rename(columns={'MONTH': 'month'})

    # Add unit to column 'Waterflow(BeforePump)'
    df = df.rename(columns={'Waterflow(BeforePump)': 'Waterflow(BeforePump) [m³/sec]'})

    # Add unit to column 'Waterflow(AfterPump)'
    df = df.rename(columns={'Waterflow(AfterPump)': 'Waterflow(AfterPump) [m³/sec]'})

    sent_messages = 0
    for index, row in df.iterrows():
        data = row.to_dict()

        # convert from datetime object to time string with iso format, example: '2008-03-05T12:00:00'
        date_str = data.pop('Date').isoformat()
        data['Date'] = date_str

        data['location_before'] = {'lat': LOCATION_BEFORE[0], 'lon': LOCATION_BEFORE[1]}
        data['location_after'] = {'lat': LOCATION_AFTER[0], 'lon': LOCATION_AFTER[1]}
        print(data)
        producer.send(KAFKA_TOPIC, data)
        sent_messages += 1

    print("Broadcasted total messages: {}".format(sent_messages))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

parse_file(EXCEL_FILE)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
