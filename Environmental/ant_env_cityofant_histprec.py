# -*- coding: utf-8 -*-
""" This code is open-sourced software licensed under the MIT license (http://opensource.org/licenses/MIT)""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Antwerp municipality. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse excel files into correct format in csv files. """
""" """
""" Data is distributed in two excel files. Each excel file has the data for 6 of the stations, a sheet per station"""
""" There is a sheet also in each file named ALLES with cleaned data for the corresponding to the 6 stations: we parse this one """
""" ALLES sheet has two columns per station (one of them is hidden), with naming of the form Pn and Pn.1 (Pn: id of the station)"""
""" We are interested in the column with name Pn""" 
""" Date time is the first column with the format YYY.MM.DD HH:mm:ss"""
""" There is a sheet in another excel file, with the names, id and location of each station"""
""" Location information is in X, Y coordinates (Belgian Lambert 72, EPSG:31370) http://http://spatialreference.org/ref/epsg/31370/"""
""" 

"""
""" Original files must be previously saved in folder temp/code_name"""
""" """
""" code: ant_env_cityofant_histprec """
""" code with numbering:  ant_env_cityofant_histprec-P1, ant_env_cityofant_histprec-P2, ant_env_cityofant_histprec-P3, ant_env_cityofant_histprec-P4, ant_env_cityofant_histprec-P5, ant_env_cityofant_histprec-P6, """
""" 					ant_env_cityofant_histprec-P7, ant_env_cityofant_histprec-P8, ant_env_cityofant_histprec-P9, ant_env_cityofant_histprec-P10, ant_env_cityofant_histprec-P11, ant_env_cityofant_histprec-P12	"""

import os
import pandas as pd
import shutil
import uuid
#import pytz
import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)
code = "ant_env_cityofant_histprec"
xlfnames =['alladata_v20_deel1.xlsx','alladata_v20_deel2.xlsx']
xlflocations = 'sensors_antwerpen.xlsx'

l_temp_path = './temp/'
l_final_path = './data/'
names_sheetn = 'sensors'
clean_data_sheetn = 'ALLES'

class ant_env_cityofant_histprec (object):

	def _init_(self):
		self.local = True

	def parse_files(self):

		try: 
			#first, parse sensor locations
			xlflocationsname = l_temp_path+code+'/'+xlflocations
			xl_l = pd.ExcelFile(xlflocationsname)
			df_stations = xl_l.parse(names_sheetn)

		except Exception as e:
			self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'data source not found or cannot be open',e)
			return False

		

		try:
			df = pd.DataFrame()
		
			#second, parse data
			for fileName in xlfnames:
				try: 		
					xlfname = l_temp_path+code+'/'+fileName#
					xl = pd.ExcelFile(xlfname)
					print ('opening file '+fileName)
				except Exception as e:
					self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'data source not found or cannot be open',e)
					return False
				
				df_clean_data = xl.parse (clean_data_sheetn)#,parse_cols=[0,2,4,6,8,10,12])
				#print (df_clean_data.columns.tolist)
				#print (df_clean_data.index)
				df_clean_data.reset_index(inplace = True)
				#print (df_clean_data.columns.tolist)
				df_clean_data.rename(columns={df_clean_data.columns[0]:'DateTime'},inplace=True)
				print (df_clean_data.columns.tolist)
				df_temp = pd.DataFrame()
				for column in df_clean_data:

					#Directory name by code/codenumber
					if column != 'DateTime' and column.find('.')!=-1:
						name =column.split(".")[0]
						#new datagram with the station values
						df_temp = df_clean_data [['DateTime',column]].copy()
						df_temp.rename(columns={column:'Rainfall'},inplace=True)
						#Format time into ISO 8601
						df_temp['DateTime'] = pd.to_datetime(df_temp['DateTime'], format='%Y-%m-%d%H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+01')
						#get the NR of the station from the name
						#s = ''.join(x for x in name if x.isdigit())
						#print ('column NR '+s)
						#get the values of the station
						yl = df_stations.loc[df_stations['NR'] == name,'Y'].item()
						xl = df_stations.loc[df_stations['NR'] == name,'X'].item()
						df_temp['Y'] = yl
						df_temp['X'] = xl
						#Note Format X Y into Latitude Longitude if needed
						#df_temp['Latitude'] = df_stations.loc[df_stations['NR'] == name,'Y'].item()#  int(s),'Latitude']
						#df_temp['Longitude'] = df_stations.loc[df_stations['NR'] == name,'X'].item()#int(s),'Longitude']
						df_temp['Location'] = df_stations.loc[df_stations['NR'] == name,'LOCATIOn'].item()#int(s),'Name']
						df_temp['NR'] = df_stations.loc[df_stations['NR'] == name,'NR'].item()
						
						df = df.append(df_temp, ignore_index=True)

			#for data model			
			df.rename(columns={'NR':'Sensor_id'},inplace=True)
		

		except Exception as e:
			self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'data source format is not as expected',e)
			return False

		try:
			#create folder/file structure
			outerdir = l_final_path+code
			if not os.path.exists(outerdir):
				os.mkdir(outerdir)
			#All the data stored in same file, same folder
			outdir=outerdir
			if not os.path.exists(outdir):
				os.mkdir(outdir)
	        #Write to the csv file.
			csvfile = str(uuid.uuid4()) + ".csv"
			print ('writing to folder '+code+'_'+name)
			fullname = os.path.join(outdir, csvfile)

			df.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False)
		except Exception as e:
			self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'cannot store data in csv file',e)
			return False


		return True


	def producer(self,topic,msg,e=None):
	""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		msg_b = str.encode(msg)
		producer.send(topic, msg_b).get(timeout=30)
		if (e):
			logging.exception('exception happened')				
	


if __name__ == '__main__':
	a = ant_env_cityofant_histprec()
	if (a.parse_files()):
		a.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_INGESTION",'Historic precipitation data for antwerp ingested to HDFS')

