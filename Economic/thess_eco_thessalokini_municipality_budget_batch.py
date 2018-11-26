# -*- coding: utf-8 -*-

"""Download data from html tables into csv, batch version (historical data )"""
""" """
""" Data is in html drivers that are displayed when choosing the adequate values in <select> elements"""
""" <select id = fyear> with option values = 2011-2018 and similar text values """
""" <select id = esex> with option values = 1,0 with text values = Έσοδα,Έξοδα  (Income,Expenses)"""
""" All the data (Income and Expenses) are stored in the same output file."""
""" Type, that is Income or Expenses, is added as a column"""
""" Year is added as a column"""
""" Greek names are translated"""
""" """
""" """

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys
import shutil
import uuid

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


origin_url = 'https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php'
code = 'thess_eco_thessaloniki_municipality_budget'

#TODO firefox webdriver
#path_to_webdriver = 'C:\\Users\\martacor\\Development\\python\\cuttler\\libs\\geckodriver.exe'
path_to_webdriver = 'C:\\Users\\martacor\\Development\\python\\cuttler\\libs\\chromedriver.exe'
options ={'Έξοδα':'Expenses','Έσοδα':'Income'} #Expenses, Income
l_temp_path = './temp/'
l_final_path = './data/'
l_temp_file = 'thessaloniki_budget.csv'
temp_path = ''
#final_path = '"/var/spoolDirectory/cutler/data/'#+code

class thess_eco_thessaloniki_municipality_budget (object):
	
	def __init__(self, url):
		self.url = url
		self.local = True
		self.file_to_move =''

	def get_session(self):
		"""Initialize webdriver and target URL, depending on environment"""
		#try: 
		if self.local:
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver)#Firefox()
			self.driver.implicitly_wait(30)
			self.driver.get(self.url)
			#self.driver = webdriver.Firefox(executable_path=path_to_webdriver)#firefox_profile=fp,firefox_options=options)
			#self.driver.implicitly_wait(15)
			#self.driver.get(self.url)
		else:
			fp = webdriver.FirefoxProfile()
			fp.set_preference("browser.download.folderList", 2)
			fp.set_preference("browser.download.manager.showWhenStarting", False)
			fp.set_preference("browser.download.dir", l_temp_path)
			fp.set_preference("browser.helperApps.neverAsk.saveToDisk","attachment/csv")
			options = Options()
			options.add_argument("--headless")
			#Initialize webdriver and target URL
			self.driver = webdriver.Firefox(firefox_profile=fp,firefox_options=options)
			self.driver.implicitly_wait(15)
			self.driver.get(self.url)
			self.verificationErrors = []
			self.accept_next_alert = True
		return self.driver
		#except:
		#	print(sys.exc_info()[0],"occured.")
		#	return False

	def parse_tables(self,driver):
		""" Parse HTML tables """
		outerdir = l_temp_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir + code
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		csvfile = l_temp_file
		
		self.file_to_move = os.path.join(outdir, csvfile)

		try:
			df_final = pd.read_csv(self.file_to_move, engine='python',encoding='utf-8-sig', sep=",")
			df_final= df_final.drop(columns='year')
			df_final= df_final.drop(columns='type')
		except:
			df_final = pd.DataFrame()
			print ('not file found')

		select = Select(driver.find_element_by_id('esex'))
		typeoptions = [to.text for to in select.options]

		for option in typeoptions:
			#Directory name by code/codenumber 
			select.select_by_visible_text (option)
			select = Select(driver.find_element_by_id('esex'))
			print('primary select')
			select_y = Select(driver.find_element_by_id('fyear'))
			yearoptions = [so.text for so in select_y.options] 

			for year in yearoptions:
				# select by visible text
				#print(year)
				select_y = Select(driver.find_element_by_id('fyear'))
				select_y.select_by_visible_text(year)
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
				#Add new columns
				#print ('add year and type') 
				df[0]['Year'] = year
				df[0]['Type'] = options[option]
				#print ('appending to df_final')
				#print (sys.stdout.encoding)
				#print ('***********************************')
				#renaming fields from greek
				df[0].rename(columns={'Υπηρεσία':'Directorate', 'Κ.Α.':'Code Number', 'Περιγραφή':'Description','Προϋπολογισθέντα':'Projected','Διαμορφωθέντα':'Actual','Δεσμευθέντα':'Commitments','Ενταλθέντα':'Payment Orders','Πληρωθέντα':'Paid','Βεβαιωθέντα':'Established','Εισπραχθέντα':'Collected'},inplace=True)
				dft=df[0]
				#print(dft.dtypes)
				#Note: Directorate value is Δεν υπάρχουν αποτελέσματα when no results
				dft['Directorate']=dft['Directorate'].astype(str)
				dft = dft[dft['Directorate']!= 'Δεν υπάρχουν αποτελέσματα']
				df_final = df_final.append(dft, ignore_index=True)
				df_final.drop_duplicates(keep='first',inplace=True)
				select_y = Select(driver.find_element_by_id('fyear'))
				
			select = Select(driver.find_element_by_id('esex'))
			
			#df_final comes from read csv first
			df_final.drop_duplicates(keep='last',inplace=True)
		df_final.to_csv(self.file_to_move, mode='w', encoding='utf-8-sig', index=False)


		#Copy the file to target folder
		path = l_final_path+code+'/'
		uFileName = str(uuid.uuid4())
		filname = path + uFileName + ".csv"
		f_outerdir = l_final_path
		if not os.path.exists(f_outerdir):
			os.mkdir(f_outerdir)
		f_outdir = f_outerdir + code
		if not os.path.exists(f_outdir):
			os.mkdir(f_outdir)
		shutil.copy(l_temp_path+code+'/'+l_temp_file, filname)
		 
	

if __name__ == '__main__':
	a = thess_eco_thessaloniki_municipality_budget(origin_url)
	d= a.get_session()
	if (d):
		a.parse_tables(d)
		#end the Selenium browser session
		d.close()
		d.quit()
