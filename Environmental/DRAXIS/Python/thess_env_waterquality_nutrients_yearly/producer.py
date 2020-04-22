import os
import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *


def parse_file(excel, sheet):
    total_messages = 0

    # All parameters has the same Unit, so no need for mapping in constants
    UNIT = 'μM'

    df = pd.read_excel(excel, sheet, header=1)

    # drop NaN columns that act like separators
    df = df.dropna(axis=1, how='all')

    # rename greek columns
    df = df.rename(columns={'Παράμετρος': 'Parameter', 'Σταθμός': 'Station'})

    # transform the DataFrame
    df = pd.melt(df, id_vars=['Parameter', 'Station'], var_name='Date', value_name='Value')

    # replace the datetime object in Date columns, that are read by-default to string
    # in order to be json encoded compatible
    df.Date = df.Date.apply(lambda x: x.strftime('%Y-%m-%d'))

    for row in df.iterrows():
        # replace original NaN values with None
        data = row[1].where(pd.notnull(row[1]), None).to_dict()

        station = data['Station'].strip()

        lat, lon = STATIONS.get(station)

        # add location
        data['location'] = {
            'lat': lat,
            'lon': lon
        }

        # add unit which is the same for all
        data['Unit'] = UNIT

        print(data)
        producer.send(KAFKA_TOPIC, data)
        total_messages += 1

    print("Broadcasted total messages: {}".format(total_messages))


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))

parse_file(EXCEL_FILE, SHEET_NAME)
# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
