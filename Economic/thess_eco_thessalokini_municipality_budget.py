# -*- coding: utf-8 -*-

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
""""""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import os
import shutil
import uuid

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


origin_url = 'https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php'
code = 'thess_eco_thessaloniki_municipality_budget'
path_to_webdriver = 'C:\\Users\\martacor\\Development\\python\\cuttler\\libs\\chromedriver.exe'
#TODO Firefox webdriver
options ={'Έξοδα':'Expenses','Έσοδα':'Income'} #Exoenses, Income
#local
l_temp_path = './temp/'
l_final_path = './data/'
l_temp_file = 'thessaloniki_budgetTEST.csv'
#TODO
temp_path = ''
final_path = '/var/spoolDirectory/cutler/data/'#+code

class thess_eco_thessaloniki_municipality_budget (object):
	
	def __init__(self, url):
		self.url = url
		self.local = True
		self.file_to_move =''


	def get_session(self):
		try: 
			driver = webdriver.Chrome(executable_path=path_to_webdriver)#Firefox()
			driver.implicitly_wait(30)
			driver.get(self.url)
			return driver
		except:
			print(sys.exc_info()[0],"occured.")
			return False

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
	

if __name__ == '__main__':
	a = thess_eco_thessaloniki_municipality_budget(origin_url)
	d= a.get_session()
	if (d):
		a.parse_tables(d)
		d.close()
		d.quit()