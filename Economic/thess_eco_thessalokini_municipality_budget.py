# -*- coding: utf-8 -*-

""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Thessaloniki Municipality (https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php). By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 


"""Download data from html tables into csv, with scheduled update"""
""" """
""" Data is in html tables that are displayed when choosing the adequate values in <select> elements"""
""" <select id = fyear> Just current option (which is current year)"""
""" <select id = esex> with option values = 1,0 with text values = Έσοδα,Έξοδα  (Income,Expenses)"""
""" All the data (Income and Expenses) are stored in the same output file."""
""" Type, that is Income or Expenses, is added as a column"""
""" Year is added as a column"""
""" Greek names are translated"""
""" Note: Directorate value is Δεν υπάρχουν αποτελέσματα when no results (sometimes retrieving one year fails)"""
""" Note: if Local is set to False, the browser runs in headless mode"""
""""""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil
import uuid
from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)
origin_url = 'https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php'
code = 'thess_eco_thessaloniki_municipality_budget'
path_to_webdriver_c = 'path_to_driver'

options ={'Έξοδα':'Expenses','Έσοδα':'Income'} #Exoenses, Income
#local
l_temp_path = './temp/'
l_final_path = './data/'
l_temp_file = 'thessaloniki_budget.csv'
WINDOW_SIZE = "1920,1080"
#TODO
temp_path = ''
final_path = '/var/spoolDirectory/cutler/data/'#+code

class thess_eco_thessaloniki_municipality_budget (object):
	
	def __init__(self, url):
		self.url = url
		self.local = False
		self.file_to_move =''


	def get_session(self):
		#try: 
		if self.local:
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c)#,chrome_options=chrome_options)
			self.driver.implicitly_wait(60)
			self.driver.maximize_window()
			self.driver.get(self.url)
		else:

			chrome_options = Options()  
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c,chrome_options=chrome_options)#,chrome_options=chrome_options)
			
			self.driver.implicitly_wait(60)
			self.driver.get(self.url)#self.verificationErrors = []
			#self.accept_next_alert = True
			#
		return self.driver
		#except:
		#	print(sys.exc_info()[0],"occured.")
		#	return False

	def parse_tables(self,driver):

		#first, get file with old values
		outerdir = l_temp_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir + code
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		csvfile = l_temp_file
	
		filename = os.path.join(outdir, csvfile)
		filename2 = os.path.join(outdir, 'temptest.csv')
		print('file name to open '+filename)


		try:
			df_old = pd.read_csv(filename, engine='python',encoding='utf-8-sig', sep=",")
		except:
			df_old = pd.DataFrame()
			print ('not file found')
		df_new = pd.DataFrame()
		select = Select(driver.find_element_by_id('esex'))
		typeoptions = [to.text for to in select.options]
		for option in typeoptions:
			#Directory name by code/codenumber 
			select.select_by_visible_text (option)
			select = Select(driver.find_element_by_id('esex'))
			#print('primary select')

			select_y = Select(driver.find_element_by_id('fyear'))
			selected_option = select_y.first_selected_option
			year = selected_option.text
			#print(year)
			
			#print('get soup level 2')
			soup_level2=BeautifulSoup(driver.page_source, 'lxml')
			#Beautiful Soup grabs the HTML table on the page
			#print('get tables')
			tables = soup_level2.find_all('table')
			#print('get just one table')
			table = tables[1]
			#Giving the HTML table to pandas to put in a dataframe object
			#read_html() produces a list of dataframes
			#print ('create dataframe list') 
			df = pd.read_html(str(table),header=0)
			#print ('add year')
			#Add new columns
			df[0]['Year'] = year
			df[0]['Type'] = options[option]
			#renaming fields in greek
			df[0].rename(columns={'Υπηρεσία':'Directorate', 'Κ.Α.':'Code Number', 'Περιγραφή':'Description','Προϋπολογισθέντα':'Projected','Διαμορφωθέντα':'Actual','Δεσμευθέντα':'Commitments','Ενταλθέντα':'Payment Orders','Πληρωθέντα':'Paid','Βεβαιωθέντα':'Established','Εισπραχθέντα':'Collected'},inplace=True)
			dft=df[0]
			#print(dft.dtypes)
			#Note: Directorate value is Δεν υπάρχουν αποτελέσματα when no results
			#cleaning the 'no values' rows
			dft['Directorate']=dft['Directorate'].astype(str)
			dft = dft[dft['Directorate']!= 'Δεν υπάρχουν αποτελέσματα']
			#print ('appending to df_old')
			df_new = df_new.append(dft, ignore_index=True)
			#print ('******new')
			#print(df_new.dtypes)
			
			#refresh select object
			select = Select(driver.find_element_by_id('esex'))	

		df_new.to_csv(filename2, mode='w', encoding='utf-8-sig', index=False)
		df_new2 = pd.read_csv(filename2, engine='python',encoding='utf-8-sig', sep=",")
		#print ('******old')
		#print (df_old.dtypes)
		#print ('******new 2')
		#print (df_new2.dtypes)
		#get just new values_ those that are in df_new2 that are not in df_old
		df_temp = pd.merge(df_new2, df_old, how='outer', indicator=True)
		rows_in_df_not_in_dfold = df_temp[df_temp['_merge']=='left_only'][df_new2.columns]
		#Create file to save new data
		#Move the changed file to target folder
		#Update stored info with new info for comparision
		if  not rows_in_df_not_in_dfold.empty:
			#print ('New rows')
			#create file
			touterdir = l_temp_path
			if not os.path.exists(touterdir):
				os.mkdir(touterdir)
			toutdir = touterdir + code
			if not os.path.exists(toutdir):
				os.mkdir(toutdir)
			csvfile =  str(uuid.uuid4()) + ".csv"
			tfilename = os.path.join(outdir, csvfile)

			#copy to
			fpath = l_final_path+code+'/'
			filname = fpath + csvfile

			#create the file with just new values
			rows_in_df_not_in_dfold.to_csv(tfilename, mode='w', encoding='utf-8-sig', index=False)
			f_outerdir = l_final_path
			if not os.path.exists(f_outerdir):
				os.mkdir(f_outerdir)
			f_outdir = f_outerdir + code
			if not os.path.exists(f_outdir):
				os.mkdir(f_outdir)
			shutil.move(l_temp_path+code+'/'+csvfile, filname)

			#add new values to old
			#print ('appending to df_old')
			df_old = df_old.append(rows_in_df_not_in_dfold, ignore_index=True)
			df_old.to_csv(filename, mode='w', encoding='utf-8-sig', index=False)
	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		topic = "THESS_ECO_THESSALONIKI_MUNICIPALITY_BUDGET_DATA_INGESTION"
		producer.send(topic, b'Thessaloniki municipality budget data ingested to HDFS').get(timeout=30)
	

if __name__ == '__main__':
	a = thess_eco_thessaloniki_municipality_budget(origin_url)
	d= a.get_session()
	if (d):
		a.parse_tables(d)
		a.producer()
		d.close()
		d.quit()
