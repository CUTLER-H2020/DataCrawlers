import os
import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *


MONTHLY_BASE_URL = "http://waterlevel.ie/data"
WATER_QUALITY_CODE = 0o001  # literal int: 0001


def broadcast_daily_data(station):
    url = "{}/day/{}_{:04d}.csv".format(MONTHLY_BASE_URL, STATIONS_ID.get(station), WATER_QUALITY_CODE)

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
    broadcast_daily_data(station_name)

# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
