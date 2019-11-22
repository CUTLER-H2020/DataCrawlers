# -*- coding: utf-8 -*-

""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Cork. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse excel file into correct format in csv files. """
""" """
"""	Data are stored in an excel file named Visitor numbers_cork.xlsx in a table"""
""" Columns names:
	-Date
	-Number of visitors
	-Number of visitors (pay)		

"""
""" Original files must be previously saved in folder temp"""
""" """



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
#codes and corresponding columns in the datasheet
code='cork_eco_visitors_daily'

l_temp_path = './temp/'
l_final_path = './data/'

xlfname = 'Visitor numbers_cork.xlsx' 


class cork_soc_visitors_daily(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (header = 0,usecols='A:C')



		#print(len(df_data.columns))
		#print (df_data.columns.tolist)

		#print (len(df_data))

		#format date correctly
		df_data['Date'] = pd.to_datetime(df_data['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')


		#columns names to comply with data models	
		df_data.rename(columns={'Number of visitors':'number_visitors','Number of visitors (pay)':'number_of_psying_visitors'},inplace=True)

				
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		csvfile = str(uuid.uuid4()) + ".csv"
		print ('writing to folder '+code)
		fullname = os.path.join(outdir, csvfile)

		df_data.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)
			
	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		topic = "CORK_ECO_VISITORS_DAILY"
		producer.send(topic, b'Cork visitors data ingested to HDFS	').get(timeout=30)
if __name__ == '__main__':
	a = cork_soc_visitors_daily()
	a.parse_file()
	a.producer()
