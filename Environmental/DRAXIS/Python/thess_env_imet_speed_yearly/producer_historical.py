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

This code is used to crawl/parse data from Thessaloniki's traffic report website (https://www.trafficthessreports.imet.gr/)
By downloading this code, you agree to contact the corresponding data provider
and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process)
all data obtained from the data source.

"""

import os
import json
import datetime
import pandas as pd
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *
from producer_daily import get_data_url, broadcast_data
from dateutil.relativedelta import relativedelta

"""
We want to crawl and insert data from 01-01-2019 until 'today' in intervals of 90 days
(That's the max time period the API allows us to download data)

After that period the daily crawler will run each day 
- from: 'yesterday'
- to: 'today'

"""

load_dotenv()

historical_producer = KafkaProducer(
    bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
    security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
    ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
    ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
    ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
    value_serializer=lambda m: json.dumps(m).encode('utf8')
)

START = datetime.datetime(2019, 1, 1)

from_date_obj = START
to_date_obj = START + relativedelta(days=90)

today_obj = datetime.datetime.today()

# Construct a list with all the dates couple, that
# we should request to get data from 01-01-2019 until 'today'
requesting_dates = []

while to_date_obj <= today_obj:
    from_date = from_date_obj.strftime('%d-%m-%Y')
    from_time = from_date_obj.strftime('%H:%M')

    to_date = to_date_obj.strftime('%d-%m-%Y')
    to_time = to_date_obj.strftime('%H:%M')

    from_date_obj = to_date_obj
    to_date_obj += relativedelta(days=90)

    requesting_dates.append([from_date, to_date])

# Finally the remaining days until today ( < 90 days)
from_date_final = from_date_obj.strftime('%d-%m-%Y')
from_time_final = from_date_obj.strftime('%H:%M')

to_date_final = today_obj.strftime('%d-%m-%Y')
to_time_final = today_obj.strftime('%H:%M')

requesting_dates.append([from_date_final, to_date_final])

# Requesting data for all the dates that we have in the list
FROM_TIME = '00:00'
TO_TIME = '00:00'

for date_couple in requesting_dates:
    from_date = date_couple[0]
    to_date = date_couple[1]

    print("Requesting from: {}".format(from_date))
    print("Requesting to: {}\n".format(to_date))

    for route, route_id in ROUTE_IDS.items():
        csv = get_data_url(route_id=route_id,
                           from_date=from_date,
                           from_time=FROM_TIME,
                           to_date=to_date,
                           to_time=TO_TIME)

        broadcast_data(route, csv, producer=historical_producer)

# Make the assumption that all messages are published and consumed
historical_producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
historical_producer.flush()
