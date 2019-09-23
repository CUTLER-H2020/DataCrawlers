# -*- coding utf-8 -*-
""" -This Crawler+Scraper requests the URL (data.gov.ie - Met Éireann)) and fetches the content of the file containing historical readings of weather condition"""
""" -The time is reported in UTC which is then converted to ISO 8601 format with UTC offset"""
""" -The available data is formatted, and   it is stored in .CSV format with unique name"""

import uuid
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)

def historicWeatherInfo():

    """This function fetches the data from the source and after cleaning stores it to .CSV file"""
    path = "" # PATH to storage directory
    uFileName = str(uuid.uuid4())
    filname = path + uFileName + ".csv"
    url = 'https://cli.fusio.net/cli/climate_data/webdata/hly1075.csv'
    df = pd.read_fwf(url)
    df_1 = df[14:] #Removes unnecessary rows contains duration of data etc.
    df_final = df_1["Station Name: ROCHES POINT"].str.split(",", n=14, expand=True) # As data is ; separated, additional formatting is done to allocate observation to their corresponding columns
    df_final.columns = ['DateTime', 'indicator_rain', 'rain', 'indicator_temp', 'temp', 'indicator_wetb', 'wetb', 'dewpt',
                   'vappr', 'rhum', 'msl', 'indicator_wdsp', 'wdsp', 'indicator_wddir', 'wddir']
    df_final['DateTime'] = pd.to_datetime(df_final['DateTime']) # Transforms available time information in string to datetime format
    df_final['DateTime'] = df_final["DateTime"].dt.strftime("%Y-%m-%dT%H:%M+00") # Transforms available time information to ISO 8601
    df_final.to_csv(filname, index = False)
def producer():
    """ This function sends data to kafka bus"""
    producer = KafkaProducer(bootstrap_servers=['10.10.2.51:9092'], api_version=(2, 2, 1))
    topic = "CORK_ENV_MET_W_DAILY_DATA INGESTION"
    producer.send(topic, b'Historical weather information for Ireland ingested to HDFS').get(timeout=30)

historicWeatherInfo()
producer()