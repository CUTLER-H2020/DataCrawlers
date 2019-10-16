""" This scripts reads data stored in HDFS directory and indexes it to Elastic Search
- To run this script Apache Spark and respective Elastic Search jars on the host machine where Apache Spark is , are required
- The indexed data can be then used for visualization
- This is at the moment is experimental"""

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SQLContext, SparkSession
import warnings
from pyspark.sql import functions*
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka import KafkaConsumer
import logging
import sys
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"
logging.basicConfig(level=logging.INFO)
"""Subscribes to data ingestion messages and picks data from HDFS folder for indexing it to ES"""
topic = 'TOPIC_NAME'
consumer = KafkaConsumer(topic, bootstrap_servers=['HOST OR HOSTS'], api_version=(2,2,1),group_id='grp')
for message in consumer:
    print (message)
    consumer.commit()
#Test for jobs to be done
sc = SparkContext(appName="ElasticHDFS")
spark = SparkSession.builder.appName("ElastHDFS").master("yarn").getOrCreate()
df = spark.read.csv("hdfs://PATH_TO_HDFS_DATA_SOURCE_DIRECTORY",mode="DROPMALFORMED", header=True)
df_1 = df.selectExpr("cast(_c0 as float)water_level", "cast(_c1 as string)Quality", "cast(_c2 as string)DateTime") #Sample line for casting values not in correct format
"""Configuration for HDFS to ELASTIC to be written based on size of data i.e. real-time batch etc"""
df_1.write.format("org.elasticsearch.spark.sql").option('es.nodes', 'HOST_IP').option('es.port',9200).option('es.batch.size.bytes','50mb').option('es.batch.size.entries','100000').option('es.write.operation','upsert').option('es.resource','ringwaterflows/ringType').mode('append').save()
"""Produces message to Kafka bus after indexing data to ES"""
producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
topic = "CORK_ENV_OPW_WL_15min_DATA_INDEXED_TO_ES"
producer.send(topic, b'Historic water levels data by the OPW for station 19069 Ringaskiddy NMCI for Cork Pilot indexed to ELASTIC SEARCH').get(timeout=30)


