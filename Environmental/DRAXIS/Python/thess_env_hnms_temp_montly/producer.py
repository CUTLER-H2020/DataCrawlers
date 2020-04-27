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

This code is used to crawl/parse data from file from Thessaloniki Municipality (11196_TEMP_THESSALONIKI.xls).
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


def parse_excel(excel):

    # the following variables apply to all rows in the excel file, so treat them as constants
    station_name = 'Macedonia'
    station_code = 16622
    location = {'lat': 40.529, 'lon': 22.9703}

    df = pd.read_excel(excel,
                       header=12,  # drop first rows that contain general info and images
                       names=['year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                              'September', 'October',
                              'November', 'December'],
                       usecols=[1, 4, 6, 7, 10, 12, 13, 14, 16, 17, 19, 20, 22],  # use the columns that map to the above months
                       decimal=',')

    # Remove outlier values of column "year" like 'Μέση Τιμή", "Μέγιστη Τιμή", "Ελάχιστη Τιμή"
    # and convert everything in the dataframe to numeric values, since "year" column was read
    # as str because of the outlier values

    df = df[pd.to_numeric(df['year'], errors='coerce').notnull()]

    # although ',' was used as a decimal, columns January, February are still str because of the
    # total weird structure of raw data (excel)
    # Changing them to float
    df.January = df.January.astype(float)
    df.February = df.February.astype(float)

    df = df.reset_index(drop=True)  # reset indexes to sequential eg. 0-179

    # Every 60 rows we have another section (max temps, min temps, mean temps)
    # break those domains in different DataFrames.
    # There is no other way to separate those logical units

    df_max = df.iloc[:60]
    df_min = df.iloc[60:120]
    df_mean = df.iloc[120:180]

    # melt those DataFrames in order to merge them into one later based on month
    # since each month will have 3 kind of temperatures
    melt_max = pd.melt(df_max, id_vars='year', var_name='month', value_name='Maximum Temperature (°C)')
    melt_min = pd.melt(df_min, id_vars='year', var_name='month', value_name='Minimum Temperature (°C)')
    melt_mean = pd.melt(df_mean, id_vars='year', var_name='month', value_name='Average Temperature (°C)')

    merged_df = melt_max.merge(melt_min, on=['year', 'month']).merge(melt_mean, on=['year', 'month'])

    sent_messages = 0
    for index, row in merged_df.iterrows():
        data = row.to_dict()

        # extract date and add it, with day as 01 by default as we ain't have the days
        data['date'] = "{}-{}-01".format(data['year'], MONTHS_MAPPING_TO_NUMBERS[data['month']])

        # add the remaining values needed for ES/Kibana
        data['station_name'] = station_name
        data['station_code'] = station_code
        data['location'] = location

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

parse_excel(EXCEL_FILE)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
