# -*- coding utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Hassan Mehmood, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from diverse shapefiles from different institutions; however it would work with any shapefile. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
"""

""" -This scripts converts the .shp shapefiles to GeoJSON format for further usage"""
""" -The available content in .shp file is extracted to get the fields name and respective data"""
""" - The file is stored in GeoJSON in the storage directory"""
import shapefile
import  pandas as pd
from pandas.io.json import json_normalize
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)
def shapeConvertor():
    """This function extracts the data from the shapefile and converts it GeoJson for further usage"""
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 2000)
    reader = shapefile.Reader("") # Add path of the file to read the content of .shp file
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
       atr = dict(zip(field_names, sr.record))
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr))
    df = json_normalize(buffer) #Removes nested structure
    path = "" # Storage directory for converted GeoJSON
    filname = path + "Name_of_file" + ".json"
    df.to_json(filname)
def producer():
    """ This function sends data to kafka bus"""
    producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
    topic = "ANT_ENV_CITYOFANT_MAPS_DATA_INGESTION"
    topic_1 = "CORK_ENV_CAR_PARKING_DATA_INGESTION"
    topic_2 = "CORK_ENV_CCC3_LAND_2014_DATA_INGESTION"
    topic_3 = "CORK_ENV_EPA_CWFD_20102015_DATA_INGESTION"
    topic_4 = "CORK_ENV_EPA_GWWFD_20102015_DATA_INGESTION"
    topic_5 = "CORK_ENV_EPA_LWFD_20102015_DATA_INGESTION"
    topic_6 = "CORK_ENV_EPA_NHA_2012_DATA_INGESTION"
    topic_7 = "CORK_ENV_EPA_RWFD_20102015_DATA_INGESTION"
    topic_8 = "CORK_ENV_EPA_SAC_2015_DATA_INGESTION"
    topic_9 = "CORK_ENV_EPA_SPA_2015_DATA_INGESTION"
    topic_10 = "CORK_ENV_EPA_TWFD_20102015_DATA_INGESTION"
    topic_11 = "CORK_ENV_OPW_FLOODS_2016_DATA_INGESTION"
    producer.send(topic, b'Antwerp Shapefiles data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_1, b'Cork car parking shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_2, b'Cork land shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_3, b'Cork CWFD shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_4, b'Cork GWWFD shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_5, b'Cork LWFD shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_6, b'Cork NHA shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_7, b'Cork RWFD shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_8, b'Cork SAC shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_9, b'Cork SPA shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_10, b'Cork TWFD shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)
    producer.send(topic_11, b'Cork OPW shapefile data in GeoJSON format ingested to HDFS').get(timeout=30)

shapeConvertor()
producer()
