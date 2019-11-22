# -*- coding: utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Thessaloniki Municipality. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse excel files into correct format in csv files. """
""" """
""" """
"""
Note, all files we have are Finalcial_Data_10_Sept_2018
Revenue: File turnover_per_sector description: (similar file in drive to esoda_ana_tomea)
Street - Sector - Turnover
(Οδός - Τομέας - Έσοδα )(Odós - Toméas - Ésoda)
BEware!! there are rows with total value
Occupacy: File  Live!Occupancy (similar file in drive is plirotita_thesewn_live)
Sector - Address - Noofspots - NoofOccupiedspots - Occupancy
(Τομέας - Διεύθυνση - Αριθμός θέσεων - Πληρωμένες θέσεις - Πληρότητα)(Toméas - Diéfthynsi - Arithmós théseon - Pliroménes théseis - Plirótita)

From Revenue, remove rows where Sector (Τομέας) is Total
From occupacy, remove rows where Sector (Τομέας) is NaN
Combine both informations by Τομέας
Leave Address (Διεύθυνση) from XX_live file (In the other file is Οδός - Street)
"""
""" Original files must be previously saved in folder temp/code_name """
""" Names of original files must be in the appropiate variables xlfrevenues and xlfoccupacies"""
""" """
""" code: thess_eco_thessaloniki_parking_data """

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
code = "thess_eco_thessaloniki_parking_data"
xlfrevenues ='esoda_ana_tomea.xls'
xlfoccupacies ='plirotita_thesewn_live.xls'


l_temp_path = './temp/'
l_final_path = './data/'

class thess_eco_thessaloniki_parking_data (object):

	def __init__(self):
		self.local = True

	def parse_files(self):

		#load the files
		xlfrevenueslocation= l_temp_path+code+'/'+xlfrevenues

		xlfoccupacieslocation= l_temp_path+code+'/'+xlfoccupacies

		df_rev = pd.read_excel(xlfrevenueslocation)
		df_occ = pd.read_excel(xlfoccupacieslocation)

		#rename columns
		df_rev.rename(columns={'Οδός':'Street','Τομέας':'Sector','Έσοδα':'Revenue'},inplace=True)
		df_occ.rename(columns={'Τομέας':'Sector','Διεύθυνση':'Address', 'Αριθμός θέσεων':'Noofspots', 'Πληρωμένες θέσεις':'NoofOccupiedspots','Πληρότητα':'Occupancy'},inplace=True) 
		
		#clean the rows
		df_rev_clean = df_rev[df_rev.Sector !='Total']
		df_occ_clean =df_occ.dropna(subset=['Sector'])

		#ensure same types in columns for merging
		df_rev_clean["Sector"] = pd.to_numeric(df_rev_clean["Sector"])
		df_occ_clean["Sector"] = pd.to_numeric(df_occ_clean["Sector"])
		#print (df_rev_clean.dtypes)
		#print (df_occ_clean.dtypes)
		#merge
		df = df_rev_clean.merge(df_occ_clean, how='outer')

		
		#save
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		outdir2 = outdir+'/'+code+'_1'
		if not os.path.exists(outdir2):
			os.mkdir(outdir2)

		#Test code
		#fullname = os.path.join(outdir2, 'rev_clean.csv')
		#df_rev_clean.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)
		#fullname = os.path.join(outdir2, 'occ_clean.csv')
		#df_occ_clean.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)	
		

        #Write to the csv file. 
		csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		print ('writing to folder '+code+'_1')
		fullname = os.path.join(outdir2, csvfile)
		df.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)

	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		topic = "THESS_ECO_THESSALONIKI_PARKING_ECONOMIC_DATA_DATA_INGESTION"
		producer.send(topic, b'THESS_ECO_THESSALONIKI_PARKING_ECONOMIC_DATA_DATA_INGESTION').get(timeout=30)
		

if __name__ == '__main__':
	a = thess_eco_thessaloniki_parking_data ()
	a.parse_files()
	a.producer()
