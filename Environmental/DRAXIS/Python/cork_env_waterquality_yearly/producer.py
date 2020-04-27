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

This code is used to crawl/parse data from file from Cork Municipality (EPA_TRaCData_CorkHarbour_2010_2018.xlsx).
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


def parse_file():
    df1 = pd.read_excel(EXCEL_FILE, SHEET1)[COLUMNS1]
    df2 = pd.read_excel(EXCEL_FILE, SHEET2)[COLUMNS2]
    # Merge the two sheets based on Station_No, keeping NaN the remaining values of non-existing stations
    df = df2.merge(df1, on="Station_No", how="left")
    pc = 0
    # The below replacements must be in this order
    # Replace irrelavant 'NR' value in column "Secchi" with 0
    df = df.replace({'Secchi': {'NR': 0}})
    # Replace all NaN values with None.
    # Essential step to broadcast the data and to be compatible with ES data types
    df = df.replace({pd.np.nan: None})

    # Convert Sample_ID from auto-detected type int to string
    df.Sample_ID = df.Sample_ID.astype('str')

    for index, row in df.iterrows():
        base = row[BASIC].to_dict()
        base['Date'] = base['Date'].date().strftime('%Y-%m-%d') if isinstance(base['Date'],
                                                                              datetime.datetime) else None
        base['Time'] = base['Time'].strftime("%H:%M:%S") if isinstance(base['Time'], datetime.time) else None
        for pol in POLLUTANTS:
            temp = {pol: row[pol],
                    'Units': UNITS[pol],
                    'Parameter_fullname': PARAMETER_FULLNAME[pol]}
            res = {**base, **temp}
            print(res)
            producer.send(KAFKA_TOPIC, res)
            pc += 1

    print("Broadcasted messages: {} of total {}".format(pc, df.shape[0] * len(POLLUTANTS)))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

parse_file()

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
