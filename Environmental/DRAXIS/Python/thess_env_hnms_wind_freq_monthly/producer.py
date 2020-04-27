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

This code is used to crawl/parse data from file from Thessaloniki Municipality (11196_WIND_FREQ_THESSALONIKI.xls).
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


def __melt_df(df):
    df = pd.melt(df, id_vars='Beaufort', var_name='Wind direction')
    return df


def parse_excel(excel):
    # the following variables apply to all rows in the excel file, so treat them as constants
    station_name = 'Macedonia'
    station_code = '16622'
    location = {'lat': 40.529, 'lon': 22.9703}  # assuming it by the other excel of "HNMS"

    df = pd.read_excel(excel,
                       header=9,  # drop first rows that contain general info and images
                       names=['Beaufort', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'CLM/VRB'],
                       usecols=[3, 6, 8, 12, 15, 18, 21, 24, 26, 28],  # use the columns that map to the above months
                       decimal=',')

    # Drop columns that 'Beaufort' column has nan values
    # Thus we manage to keep only columns in range 0,1,2,...,>9
    df = df.dropna(subset=['Beaufort'])

    df = df.reset_index(drop=True)  # reset indexes to sequential 0-119

    df['Beaufort'].replace({'>= 9': '9'}, inplace=True)  # replace outlier value '>= 9' with 9

    # The tricky thing here, is that in the raw data we have a only a logical separator
    # for the 12 months. Every 9 rows we have another section which implies another month
    # in sequential order, eg Jan, Feb,..., Dec

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
              'September', 'October',
              'November', 'December']
    month_iter = iter(months)

    month_counter = 0

    month = next(month_iter)  # start with January

    sent_messages = 0
    for index, row in df.iterrows():

        row_dict = row.to_dict()
        # Beaufort is the same for all wind directions (columns) I need to iterate
        beaufort = row_dict.pop('Beaufort')

        # If rows that are processsed are more than 9 that means, we're in the next month
        # so get next month and start the counter from the beginning
        if month_counter > 9:
            try:
                month = next(month_iter)
                month_counter = 0  # new month starts
            except StopIteration:
                break

        # after pop row contains only the winds
        for wind_direction, value in row_dict.items():

            # populate with all the constants
            payload = {
                'month': month,
                'station_name': station_name,
                'station_code': station_code,
                'location': location,
                'Beaufort': beaufort,
                'Wind direction': wind_direction,
                'Value': value
            }

            print(payload)
            producer.send(KAFKA_TOPIC, payload)
            sent_messages += 1

        # counter how many rows are processed.
        month_counter += 1

    print("Broadcasted total messages: {}".format(sent_messages))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

parse_excel(EXCEL_FILE)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
