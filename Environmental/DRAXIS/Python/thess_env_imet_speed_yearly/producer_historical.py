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
