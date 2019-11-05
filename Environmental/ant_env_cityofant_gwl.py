# -*- coding: utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Antwerp Municipality. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse excel files into correct format in csv files. """
""" """
"""	Data is stored in an excel file named Export_CUTLER_v40.xlsx in different sheets """
""" Notes on the data:
	1 Number of sensors
		In the data sheet (export) there is data on sensors that are not in the sensors sheet
		In the sensors sheet (overview) there are sensors that do not have data in the data sheet
		The information is merged according to the sensors described in the sensor sheet, and the rest is discarded
		location is expresed in  X, Y WGS84 (https://epsg.io/4326)
	2 Remarks column
		In the data sheet there us a remarks column that has been kept as it is
"""
""" Original files must be previously saved in folder temp/code_name"""
""" """
""" code: ant_env_cityofant_gwl """
""" code with numbering:  ant_env_cityofant_gwl-1, ant_env_cityofant_gwl-460"""


import os
import pandas as pd
import shutil
import uuid
from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)
code= 'ant_env_cityofant_gwl' 

l_temp_path = './temp/'
l_final_path = './data/'
sensors_sheetn = 'overview'
clean_data_sheetn = 'export'

xlfname = 'Export_CUTLER_v40.xlsx'

class ant_env_cityofant_gwl(object):

	def _init_(self):
		self.local = True

	def parse_files(self):
		fileName = l_temp_path+code+'/'+xlfname#
		xl = pd.ExcelFile(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_clean_data = xl.parse (clean_data_sheetn)
		#sensor data into dataframe
		df_sensors = xl.parse (sensors_sheetn)
		
		#First cleaning of sensor data column names 
		df_sensors.columns = df_sensors.columns.str.replace(r"\(.*\)","")#remove all braces and data inside
		#print (df_sensors.columns.tolist)

		#get only the rows of interest
		df_sensors_clean = df_sensors[['ID','Height well ', 'Height ground level ', 'Location','X ','Y ', 'X-coordinate ','Y-coordinate ']].copy()

		#all the values in the columns that will work as merging keys, need to be of the same type 
		df_clean_data["ID"] = df_clean_data["ID"].astype(str)
		df_sensors_clean["ID"] = df_sensors_clean["ID"].astype(str)

		#we merge, with the ID values of the sensors data
		df_merge = pd.merge(df_clean_data,df_sensors_clean, on ='ID', how='right')

		#sensord dataframes has 460 unique values as ID
		#UniqueNames = df_sensors_clean.ID.unique()
		#print ('sensors'+str(len(UniqueNames)))
		#merged has the same
		UniqueNames_merged = df_merge.ID.unique()
		print ('merged'+str(len(UniqueNames_merged)))


		#df_merge_clean['Date'] = pd.to_datetime(df_merge_clean['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

		df_merge.rename(columns={'Peil_cor2':'Water level','X ':'Longitude','Y ':'Latitude','Height well ':'Height well','X-coordinate ':'X','Y-coordinate ':'Y'},inplace=True)
		#n=df_clean_data['ID'].count()
		#print ('df_clean_data rows '+str(n))
		m=df_merge['ID'].count()
		print ('df_merge rows '+str(m))
		#m=df_merge_clean['ID'].count()
		#print ('df_merge_clean rows '+str(m))

		#save
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		#
		#debugging
		#csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		#print ('writing to folder '+code)
		#fullname = os.path.join(outdir, csvfile)

		#df_merge.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)


		index = 1
		count = 0
		for elem in UniqueNames_merged:
			df_temp =    df_merge[:][df_merge.ID == elem]  
			#df_temp['Date'] = pd.to_datetime(df_temp['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
			count += df_temp.count()
			outdir2 = outdir+'/'+code+'_'+str(index)
			if not os.path.exists(outdir2):
				os.mkdir(outdir2)

	        #Write to the csv file. Note, put this out of the loop to write all the sheets in same csv file
			csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
			#print ('writing to folder '+code+'_'+str(index))
			fullname = os.path.join(outdir2, csvfile)
			df_temp.rename(columns={'ID':'Sensor code'},inplace=True)
			df_temp.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)
			index+=1
		print (count)

	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		topic = "ANT_ENV_CITYOFANT_GWL_DATA_INGESTION"
		producer.send(topic, b'	GWL data for antwerp ingested to HDFS').get(timeout=30)

if __name__ == '__main__':
	a = ant_env_cityofant_gwl()
	a.parse_files()
	a.producer()
