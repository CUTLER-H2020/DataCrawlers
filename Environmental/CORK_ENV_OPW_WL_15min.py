# -*- coding utf-8 -*-
""" -This Crawler+Scraper requests the URL (OPW sensor network- Water levels)) and fetches the content of the txt file containing historical readings of water levels"""
""" -The recieved content is then parsed for available data"""
""" -The time is reported in UTC which is then converted to ISO 8601 format with UTC offset"""
""" -The data is cleaned for available special characters"""
""" - After cleaning data, it is stored in .CSV format with unique name"""
import uuid
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)
def getWaterLevel():

    """This function fetches the data from the source and after cleaning stores it to .CSV file"""
    path = "" # PATH to storage directory
    uFileName = str(uuid.uuid4())
    filname = path + uFileName + ".csv"
    url = 'http://waterlevel.ie/hydro-data/stations/19069/Parameter/S/complete.zip'
    df = pd.read_csv(url, compression="zip", sep='\s+', header=None, dtype='unicode')
    df_1 = df[7:] #Removes unnecessary rows contains duration of data etc.
    df_1.columns = ['Date', 'Time', 'water_level', 'Quality']
    df_final = df_1.copy()
    df_final["DateTime"] = pd.to_datetime(df_final["Date"].astype(str) + " " + df_final["Time"].astype(str))
    del df_final["Date"], df_final["Time"]
    df_final['DateTime'] = df_final["DateTime"].dt.strftime("%Y-%m-%dT%H:%M+00") # Transforms available time information to ISO 8601
    df_final['Quality'] = df_final['Quality'].str.replace('*', 'NA') # Replaces * values as missing values with NA
    df_final["station_id"] = "19069 Ringaskiddy" #Adds station identifier
    df_final.to_csv(filname, index=False)

def producer():
    """ This function sends data to kafka bus"""
    producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
    topic = "CORK_ENV_OPW_WL_15min_DATA_INGESTION"
    producer.send(topic, b'Historic water levels data by the OPW for station 19069 Ringaskiddy NMCI for Cork Pilot ingested to HDFS').get(timeout=30)

getWaterLevel()
producer()
