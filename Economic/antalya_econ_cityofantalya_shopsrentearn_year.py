# -*- coding: utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Antalya. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse excel files into correct format in csv files. """
""" """
""" Data are stored in an excel file named antalya_cutler_all_data_ (version 1).xlsx in different sheets """
""" Sheet name:

	- ECON_SHOP_RENT
"""
""" Original files must be previously saved in folder temp"""
""" """
""" code: anta_eco_citiofantalya_ShopsRentEarn_year """



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
code= 'anta_eco_citiofantalya_ShopsRentEarn_year' 

l_temp_path = './temp/'
l_final_path = './data/'
data_sheetn = 'ECON_SHOP_RENT'

xlfname = 'antalya_cutler_all_data_ (version 1).xlsx'


class anta_eco_ShopsRentEarn_year(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (data_sheetn,header = 1,usecols='A:B')

		#remove index columns
		df_data.reset_index(inplace = True)

		
		df_data.rename(columns={df_data.columns[1]:'Year',df_data.columns[2]:'shop_rent'},inplace=True)

		df_data = df_data[['Year','shop_rent']].copy()


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
		topic = "ANTA_ECO_CITIOFANTALYA_SHOPSRENTEARN_YEAR"
		producer.send(topic, b'Antalya duden shop rental data ingested to HDFS').get(timeout=30)


if __name__ == '__main__':
	a = anta_eco_ShopsRentEarn_year()
	a.parse_file()
	a.producer()
