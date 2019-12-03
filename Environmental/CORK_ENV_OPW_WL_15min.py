# -*- coding utf-8 -*-
""" This code is open-sourced software licensed under the MIT license (http://opensource.org/licenses/MIT)""" 
""" Copyright  2019 Hassan Mehmood, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from WaterLevel OPW (http://waterlevel.ie). By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

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

def producer(topic,msg,e=None):
""" This function sends data to kafka bus"""
    producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
    msg_b = str.encode(msg)
    producer.send(topic, msg_b).get(timeout=30)
    if (e):
        logging.exception('exception happened')   

def getWaterLevel():

    """This function fetches the data from the source and after cleaning stores it to .CSV file"""
    path = "" # PATH to storage directory
    uFileName = str(uuid.uuid4())
    filname = path + uFileName + ".csv"

    try:
        url = 'http://waterlevel.ie/hydro-data/stations/19069/Parameter/S/complete.zip'
        df = pd.read_csv(url, compression="zip", sep='\s+', header=None, dtype='unicode')
    except Exception as e:
        producer("CORK_ENV_OPW_WL_15min_DATA_INGESTION",'data source not found or cannot be open',e)
        return False
    try:
        df_1 = df[7:] #Removes unnecessary rows contains duration of data etc.
        df_1.columns = ['Date', 'Time', 'water_level', 'Quality']
        df_final = df_1.copy()
        df_final["DateTime"] = pd.to_datetime(df_final["Date"].astype(str) + " " + df_final["Time"].astype(str))
        del df_final["Date"], df_final["Time"]
        df_final['DateTime'] = df_final["DateTime"].dt.strftime("%Y-%m-%dT%H:%M+00") # Transforms available time information to ISO 8601
        df_final['Quality'] = df_final['Quality'].str.replace('*', 'NA') # Replaces * values as missing values with NA
        df_final["station_id"] = "19069 Ringaskiddy" #Adds station identifier
    except Exception as e:
        producer("CORK_ENV_OPW_WL_15min_DATA_INGESTION",'data source format is not as expected',e)
        return False
    try:    
        df_final.to_csv(filname, index=False)
    except Exception as e:
        producer("CORK_ENV_OPW_WL_15min_DATA_INGESTION",'cannot store data in file')
        return False
    return True  

if(getWaterLevel()):
    producer("CORK_ENV_OPW_WL_15min_DATA_INGESTION",'Historic water levels data by the OPW for station 19069 Ringaskiddy NMCI for Cork Pilot ingested to HDFS')
