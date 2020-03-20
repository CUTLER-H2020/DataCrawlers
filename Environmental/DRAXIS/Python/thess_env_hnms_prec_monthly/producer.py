import os
import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *


def parse_excel(excel):

    # the following variables apply to all rows in the excel file, so treat them as constants
    station_name = 'Mikra/Airport'
    station_code = '16622'
    location = {'lat': 40.529, 'lon': 22.9703}  # assuming it by the other excel of "HNMS"

    df = pd.read_excel(excel, header=8,
                       names=['year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                              'September', 'October',
                              'November', 'December'], usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    # Remove outlier values of column "year" like 'Διευκρίνιση:"
    # and convert everything in the dataframe to numeric values, since "year" column was read
    # as str because of the outlier values
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    # keep rows that their year value is between 1961 and 2018
    # thus we drop nan values from previous "to_numeric" operation
    df = df[df['year'].between(1961, 2018)]

    # For Kibana visualizations reasons, we want year as str
    # Make it int to remove decimals and then to str
    df['year'] = df['year'].astype(int).astype(str)

    # Replace nan values with None
    df = df.where(pd.notnull(df), None)

    melted_df = pd.melt(df, id_vars=['year'], var_name=['month'], value_name='Precipitation (mm)')

    sent_messages = 0
    for index, row in melted_df.iterrows():
        data = row.to_dict()

        # extract date from year and month and add it to payload

        datetime_obj = datetime.datetime.strptime("{}-{}".format(data['year'], data['month']), "%Y-%B")
        date = datetime_obj.isoformat()  # save it as str with timestamp eg. '1961-01-01T00:00:00'

        data['date'] = date

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
