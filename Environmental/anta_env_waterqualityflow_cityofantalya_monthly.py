""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Antalya Municipality. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse excel file into correct format in csv files. """
""" """
"""	Data are stored in an excel file named anta_water_quality&flow_2018_2019.xlsx in a table"""

"""
- Cleans the columns names  (removes units and other info) 
- transforms floats from , to . representation where needed
- Date to correct format
- Rename to correct model representation
"""

""" Original files (anta_water_quality&flow_2018_2019.xlsx) must be previously saved in folder temp"""
""" """
""" code: anta_env_waterqualityflow_citiofantalya_monthly """


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
l_temp_path = './temp/'
l_final_path = './data/'

xlfname = 'anta_water_quality&flow_2018_2019.xlsx' 

code = 'anta_env_waterqualityflow_citiofantalya_monthly'


class anta_env_waterqualityflow_citiofantalya_monthly(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (header = 0)

		#remove index columns
		#df_data.reset_index(inplace = True)

		
		#df_data.rename(columns={df_data.columns[0]:'Year',df_data.columns[1]:'Month'},inplace=True)
		#df.index = pd.Series(df.index).fillna(method='ffill')

		#df_data.Year = pd.Series(df_data.Year).fillna(method='ffill')

		#First cleaning of sensor data column names

		df_data.columns = df_data.columns.str.replace(r"\(.*\)","")#remove all braces and data inside
		df_data.columns = df_data.columns.str.replace(r"\n","")

		#clean data, to correct float
		df_data.replace(',', '.', regex=True,inplace=True)

		print(len(df_data.columns))
		print (df_data.columns.tolist)

		print (len(df_data))




		#Any date to reformat?	
		df_data['DATE'] = pd.to_datetime(df_data['DATE'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

		
		#rename to correct model representation
		df_data.rename(columns={'DATE':'Date','ZONE':'Zone','Lat':'Latitude','Long':'Longitude','BOD ':'conc_BOD','Dissolved Oxygen ':'conc_DO','Fecal coliform':'conc_fec_colif','Fecal Streptococcus':'conc_fec_strept','COD ':'conc_COD','pH':'pH','Total Nitrogen':'conc_N','Total Coliform':'conc_tot_colif','Total Phosphorus ':'conc_P','Volumetric Flow ':'water_volumetric_flow_rate','Water velocity ':'water_velocity'},inplace=True)
			 	 					 	 

		#save
		
			
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		print ('writing to folder '+code)
		fullname = os.path.join(outdir, csvfile)

		df_data.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)
	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		topic = "ANTA_ENV_WATERQUALITYFLOW_CITYOFANTALYA_MONTHLY_DATA_INGESTION"
		producer.send(topic, b'Antalya historical water quality data ingested to HDFS').get(timeout=30)


if __name__ == '__main__':
	a = anta_env_waterqualityflow_citiofantalya_monthly()
	a.parse_file()
	a.producer()
