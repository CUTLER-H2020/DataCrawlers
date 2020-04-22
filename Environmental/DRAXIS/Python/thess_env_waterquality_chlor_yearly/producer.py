import os
import json
import pandas as pd
import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv
from constants import *

"""
There are two methods for parsing the data from excel
one for each sheet. The reason is that each sheet does not follow
a particular structure for the data, so the "algorithm" for scraping
will be different

"""


def parse_sheet_lp_chl_a(excel, lp_sheet, total_messages):
    # Check the following for the arguments
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html

    df = pd.read_excel(excel,
                       sheet_name=lp_sheet,
                       usecols=[1, 2, 3, 4, 5, 6],  # drop unnecessary first column which is Year
                       names=['Date', 'Station', 'Location', 'Sampling Depth (m)', 'Chl-a (μg/l)', 'Chl-a (RFU)'])

    # replace the outlier value "Νοέ-15" with the corresponding conclusive date of datetime object
    df['Date'] = df['Date'].replace("Νοέ-15", datetime.datetime.strptime("2015-11-01", "%Y-%m-%d"))

    # replace the datetime object in Date columns, that are read by-default to string
    # in order to be json encoded compatible
    df.Date = df.Date.apply(lambda x: x.strftime('%Y-%m-%d'))

    # replace the misstypes station names values with the corresponding conclusive station
    # example: L2 should be -> LP2
    # Eventually this is handled with manual editing instead of doing:
    # df.Station = df.Station.replace({'L2': 'LP2', 'L3': 'LP3', 'L4': 'LP4', 'L5': 'LP5'})

    # Add extra column "month" which is populated by the extraction of month in Date field
    df['month'] = pd.DatetimeIndex(df.Date).month

    # Change it from type int to the desired type string
    df.month = df.month.astype('str')

    for row in df.iterrows():
        data = row[1].to_dict()

        station = data['Station'].strip()

        lat, lon = STATIONS.get(station)

        # prepare beforehand the location attribute to match the appropriate form
        # for geo_points in elasticsearch
        data['location'] = {
            'lat': lat,
            'lon': lon
        }

        print(data)
        producer.send(KAFKA_TOPIC, data)
        total_messages += 1
    return total_messages


def parse_sheet_sp_chl_a(excel, sp_sheet, total_messages=0):
    df = pd.read_excel(excel,
                       sheet_name=sp_sheet,
                       header=2,
                       usecols=[1, 2, 3, 4, 5, 6],  # drop unnecessary first column which is Year
                       names=["Date", "SP1", "SP2", "SP3", "SP4", "SP5"])

    # replace the datetime object in Date columns, that are read by-default to string
    # in order to be json encoded compatible
    df.Date = df.Date.apply(lambda x: x.strftime('%Y-%m-%d'))

    # restructure df to: Year, Date, Station, Chl-a (μg/l)
    # to match (almost) the basic structure of first sheet
    # in order to process data with consistency in consumer
    df = pd.melt(df, id_vars=["Date"], var_name="Station", value_name="Chl-a (μg/l)")

    # Add extra column "month" which is populated by the extraction of month in Date field
    df['month'] = pd.DatetimeIndex(df.Date).month

    # Change it from type int to the desired type string
    df.month = df.month.astype('str')

    for row in df.iterrows():
        data = row[1].to_dict()
        station = data['Station'].strip()

        lat, lon = STATIONS.get(station)

        # add location
        data['location'] = {
            'lat': lat,
            'lon': lon
        }

        print(data)
        producer.send(KAFKA_TOPIC, data)
        total_messages += 1

    return total_messages


load_dotenv()

producer = KafkaProducer(bootstrap_servers=["{}:{}".format(os.getenv('KAFKA_HOST'), os.getenv('KAFKA_PORT'))],
                         security_protocol=os.getenv('KAFKA_SECURITY_PROTOCOL', 'PLAINTEXT'),
                         ssl_cafile=os.getenv('KAFKA_CA_FILE', None),
                         ssl_certfile=os.getenv('KAFKA_CERT_FILE', None),
                         ssl_keyfile=os.getenv('KAFKA_KEY_FILE', None),
                         value_serializer=lambda m: json.dumps(m).encode('utf8'))
sent_total_messages = 0

sent_total_messages = parse_sheet_lp_chl_a(EXCEL_FILE, FIRST_LP_SHEET, sent_total_messages)

sent_total_messages = parse_sheet_sp_chl_a(EXCEL_FILE, SECOND_SP_SHEET, sent_total_messages)

print("Sent total messages: {}".format(sent_total_messages))
# Make the assumption that all messages are published and consumed
producer.send(KAFKA_TOPIC_FINISH, 'All messages are published and consumed successfully!')
producer.flush()
