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

This code is used to crawl/parse data from several file from Thessaloniki Municipality (2016_CTDatAl_public.xlsx,
2017_CTDatAl_public.xlsx, 2018_CTDatAl_public.xlsx, 2019_CTDatAl_public.xlsx).
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


def parse_file(excel_file: str, months: list, date_mapping: dict):

    messages = 0
    print("\nParsing data for excel: {}\n".format(excel_file))

    # just one month for debugging only
    # months = ['IAN16']

    for month in months:
        df = pd.read_excel(excel_file, month)

        # Make the columns -> rows but keep Station and Depth (m) for grouping reasons in Kibana
        df = pd.melt(df, id_vars=["Station", "Depth (m)"], var_name="Parameter", value_name="Value")
        print("\nSending data for month: {}\n".format(month))
        for row in df.iterrows():

            # skip all nan rows (which act like separators)
            # if pd.isna(row[1]).all():
            #     continue

            # replace original NaN values with None
            data = row[1].where(pd.notnull(row[1]), None).to_dict()

            if data['Station'] is not None:
                if data['Station'].strip() in STATIONS.keys():
                    current_station = data['Station'].strip()

            data['Station'] = current_station

            # start populating with extra fields, required for ES
            lat, lon = STATIONS[data['Station']]
            data['lat'] = lat
            data['lon'] = lon

            date_str = date_mapping.get(month)
            datetime_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            data['date'] = datetime_obj.isoformat()
            data['year'] = datetime_obj.year

            data['Parameter_fullname'] = PARAMETERS_FULLNAME_MAPPING[data['Parameter']]

            data['Location'] = STATIONS_LOCATIONS[data['Station']] if data['Station'] in STATIONS_LOCATIONS else None

            data['Unit'] = PARAMETERS_UNIT_MAPPING[data['Parameter']]

            print(data)
            messages += 1
            producer.send(KAFKA_TOPIC, data)

    print("\nPublished total messages: {}".format(messages))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

# crawl data for 2016
parse_file(EXCEL_2016, MONTHS_SHEETS_2016, DATES_2016_MAPPING)

# crawl data for 2017
parse_file(EXCEL_2017, MONTHS_SHEETS_2017, DATES_2017_MAPPING)

# crawl data for 2018
parse_file(EXCEL_2018, MONTHS_SHEETS_2018, DATES_2018_MAPPING)

# crawl data for 2019
parse_file(EXCEL_2019, MONTHS_SHEETS_2019, DATES_2019_MAPPING)

producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
