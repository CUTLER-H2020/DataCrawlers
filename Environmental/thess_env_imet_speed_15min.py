
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Thessaloniki traffic (https://www.trafficthessreports.imet.gr/). By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

"""
https://www.trafficthessreports.imet.gr/user_login.aspx
NOTE: when opening with https://www.trafficthessreports.imet.gr/export.aspx:
---> shows login page BUT redirects to desired page


Login and password  SHOULD be in an .env FILE IN SAME FOLDER as 
TRAFFIC_EMAIL=email_account
TRAFFIC_PASSWORD=password


PATH to chrome webdriver should be in variable path_to_webdriver_c

login form: 
-input name="Login1$UserName" id ="Login1_UserName"
-input name ="Login1$Password" id="Login1_Password"

-input name="Login1$LoginButton" id="Login1_LoginButton"

Routes:
1. Εγνατία (Συντριβάνι - Πλατεία Δημοκρατίας)
2. Εγνατία (Πλατεία Δημοκρατίας - Συντριβάνι)
8. Δραγούμη
9. Βενιζέλου.

This crawler is for collecting data every 15 minutes. It will query for data from 15 minutes before to now and now.

NOTE: if data are to be written to the same file as batch, remove headers when writing to csv file

NOTE: self.local = True, if browser can be open. Set to False if no browser window should be open (run in headless mode)

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging
import re
import pandas as pd
import datetime
import os
import shutil
import uuid
import time
from datetime import timedelta, date

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


basic_url = 'https://www.trafficthessreports.imet.gr'
origin_url = basic_url+'/export.aspx'
logging.basicConfig(level=logging.INFO)
code = 'thess_env_imet_speed_15min'

path_to_webdriver_c = path_to_chrome_webdriver

#where the files are temporaly downloaded
downloadFileFolder = './temp/thess_env_imet_speed_15min/'
#downloadFilepath = os.path.normpath('.//temp//')#+os.sep
final_path = './data/thess_env_imet_speed_15min'

routes = ["1. Εγνατία (Συντριβάνι - Πλατεία Δημοκρατίας)","2. Εγνατία (Πλατεία Δημοκρατίας - Συντριβάνι)","8. Δραγούμη","9. Βενιζέλου"]


startTime =""
endTime =""
startDate =""
endDate =""

class element_has_href_value(object):
	"""An expectation for checking that an element has a particular value in the href.
	locator - used to find the element
	returns the WebElement once it has the particular css class
	"""

	def __init__(self, locator, href_value):
		self.locator = locator
		self.css_class = css_class

	def __call__(self, driver):
		element = driver.find_element(*self.locator) 
		# Finding the referenced element
		if self.href_value in element.get_attribute("href"):
			return element
		else:
			return False

class thess_env_imet_speed_15min_batch (object):
	
	def __init__(self, url):
		self.url = url
		self.local = False
		self.names =[]
		load_dotenv()

	def get_session(self):
		"""Initialize webdriver and target URL, depending on environment"""
		#try: 
		if self.local:
			chrome_options = Options()
			#os.makedirs(downloadFilepath)
			mainPath = os.getcwd()
			downloadFilepath = os.path.normpath(mainPath+downloadFileFolder)
			print(downloadFilepath)
			preferences = {"profile.default_content_settings.popups": 0,'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory": downloadFilepath ,"download.prompt_for_download": False }#,"directory_upgrade": True,"safebrowsing.enabled": True }
			chrome_options.add_experimental_option("prefs", preferences)
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c,chrome_options=chrome_options)
			
			self.driver.get(self.url)
			self.driver.implicitly_wait(60)
			self.driver.maximize_window()
			#self.driver.implicitly_wait(30)
			self.driver.get(self.url)
			#self.driver = webdriver.Firefox(executable_path=path_to_webdriver)#firefox_profile=fp,firefox_options=options)
			#self.driver.implicitly_wait(15)
			#self.driver.get(self.url)
		else:

			chrome_options = Options()  
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
			#chrome_options.put("download.default_directory",downloadFilepath); 
			mainPath = os.getcwd()
			downloadFilepath = os.path.normpath(mainPath+downloadFileFolder)
			preferences = {"download.default_directory": downloadFilepath ,"directory_upgrade": True,"safebrowsing.enabled": True }
			chrome_options.add_experimental_option("prefs", preferences)
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c,chrome_options=chrome_options)#,chrome_options=chrome_options)
			
			self.driver.get(self.url)
			self.driver.implicitly_wait(60)
			#self.driver.maximize_window()
			#self.driver.implicitly_wait(30)
			self.driver.get(self.url)#self.verificationErrors = []
			#self.accept_next_alert = True
			#
		return self.driver
		#except:
		#	print(sys.exc_info()[0],"occured.")
		#	return False

	def fill_login(self):
		"""
		Fill the login''
		id ="Login1_UserName"
		id="Login1_Password"
		"""
		TRAFFIC_KEY = os.getenv("TRAFFIC_EMAIL")
		TRAFFIC_PASSWORD = os.getenv("TRAFFIC_PASSWORD")
		self.driver.find_element_by_id("Login1_UserName").send_keys(TRAFFIC_KEY)#"martacor@edu.oulu.fi")
		self.driver.find_element_by_id("Login1_Password").send_keys(TRAFFIC_PASSWORD)#"pass1234")

		self.driver.find_element_by_id("Login1_LoginButton").click()

	def get_info(self):
		"""
		id ="ExportDropDownList"
		"""

		self.fill_login()
		#wait until correct page loaded
		


		routenum = 0
		for routeName in routes:
			print (repr(routenum))

			routenum=routenum+1
			notdone = True
			i=0
			wait = WebDriverWait(self.driver, 10)
			while notdone:
			
				try:
					element = wait.until(EC.presence_of_element_located((By.XPATH,"""//*[@id="ExportDropDownList"]""")))

					notdone = False
				except:
					if (i<10):
						notdone= True
						i+=1
					else:
						print ('info took too long to load; not today')
						notdone = False
						break
			notdone = True
			#if(notdone==False):
				#filter_routes = Select( filter_panel.find_element_by_css_selector("select.form-control#filter-brands[name='filter_brands']") )
				#filter_routes.dfilter_brands.select_by_visible_text("ABC") 

				#filter_panel.find_element_by_xpath("//select[@id='ExportDropDownList']/optgroup[@label='Ταχύτητες']//option[@value='1. Εγνατία (Συντριβάνι - Πλατεία Δημοκρατίας)']").click()

				#('//optgroup[@label="Summary"]')
			
			#First, select the route

			select = Select(self.driver.find_element_by_id('ExportDropDownList'))
			option = select.select_by_visible_text(routeName)



			print('set dates')
			#Second, select the dates. Structure:
			#<div id="UpdatePanelForHiddenFields">
	        #  <input type="hidden" name="FromDateHiddenField" id="FromDateHiddenField" value="01-01-2017">
	        #  <input type="hidden" name="FromTimeHiddenField" id="FromTimeHiddenField" value="00:56">
	        #  <input type="hidden" name="ToDateHiddenField" id="ToDateHiddenField" value="26-02-2019">
	        #  <input type="hidden" name="ToTimeHiddenField" id="ToTimeHiddenField" value="09:50">
	        #</div>

			
			##SET FOR ALL THE NECESSARY DATES
			
			now = datetime.datetime.now()
			minbefore= now - datetime.timedelta(minutes=15)

			startDate= minbefore.strftime("%d-%m-%Y")
			startTime = minbefore.strftime("%H:%M")

			endDate =now.strftime("%d-%m-%Y")
			endTime =now.strftime("%H:%M")

			

			"""now = datetime.datetime.now()#.replace(hour=0, minute=0,second=0)
			endDate = now.strftime("%d-%m-%Y")
			endTime = now.strftime("%H:%M")
			"""
			
			"""<input type="hidden" name="FromDateHiddenField" id="FromDateHiddenField" value="01-01-2017"> """
			self.driver.execute_script("document.getElementsByName('FromDateHiddenField')[0].value='"+startDate+"'")
			"""<input type="hidden" name="FromTimeHiddenField" id="FromTimeHiddenField" value="00:56">"""
			self.driver.execute_script("document.getElementsByName('FromTimeHiddenField')[0].value='"+startTime+"'")
			"""<input type="hidden" name="ToDateHiddenField" id="ToDateHiddenField" value="26-02-2019"> """
			self.driver.execute_script("document.getElementsByName('ToDateHiddenField')[0].value='"+endDate+"'")
			"""<input type="hidden" name="ToTimeHiddenField" id="ToTimeHiddenField" value="09:50">"""
			self.driver.execute_script("document.getElementsByName('ToTimeHiddenField')[0].value='"+endTime+"'")
		
			"""<input type="hidden" name="FromDateHiddenField" id="FromDateHiddenField" value="01-01-2017"> """
			#self.driver.execute_script("document.getElementById('FromDate').value='"+startDate+"'")
			"""<input type="hidden" name="FromTimeHiddenField" id="FromTimeHiddenField" value="00:56">"""
			#self.driver.execute_script("document.getElementById('FromTime').value='"+startTime+"'")
			"""<input type="hidden" name="ToDateHiddenField" id="ToDateHiddenField" value="26-02-2019"> """
			#self.driver.execute_script("document.getElementById('ToDate').value='"+endDate+"'")
			"""<input type="hidden" name="ToTimeHiddenField" id="ToTimeHiddenField" value="09:50">"""
			#self.driver.execute_script("document.getElementById('ToTime').value='"+endTime+"'")

			time.sleep(5)
			print('dates done')
			fromDate= self.driver.find_element_by_name('FromDateHiddenField')
			print(fromDate.get_attribute('value'))

			#this cancels the bindHiddenFields() function. That funtion would substitute the data we have written in the hidden
			#fields with the default ones  
			self.driver.execute_script("bindHiddenFields = function bindHiddenFields() { return true;}")


			""" Button: Press to ask for the file"""
			print ("button ")
			button = self.driver.find_element_by_xpath("""//*[@id="ExportButton"]""")


			#button.click()
			actions = ActionChains(self.driver)
			actions.move_to_element(button).click(button)
			actions.perform()



			''' Wait for & get Result '''
			

			time.sleep(5)

			notdone = True
			i=0
			wait = WebDriverWait(self.driver, 10)
			while notdone:
			
				try:
					element = wait.until(EC.presence_of_element_located((By.XPATH,"""//*[@id="UpdatePanel1"]/a[2]""")))
					notdone = False
				except:
					if (i<6):
						notdone = True
						i+=1
					else:
						print ('info took too long to load; not today')
						notdone = False


			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


			anchor = self.driver.find_element_by_xpath("""//*[@id="UpdatePanel1"]/a[2]""")
			anchor.click()

			time.sleep(10)

		print ("Done downloading new data")

		
	def copy_files(self):
		mainPath = os.getcwd()
		downloadFilepath = os.path.normpath(mainPath+downloadFileFolder)
		#f = []
		for (dirpath, dirnames, filenames) in os.walk(downloadFilepath):
			#f.extend(filenames)
			sT = startTime.replace(":", "_")
			eT = endTime.replace(":", "_")
			for filename in filenames:
				index = [i for i, s in enumerate(routes) if (s in filename and startDate in filename and endDate in filename and sT in filename and eT in filename)]
				print ("route number" + repr(index))

				old_name = os.path.join(dirpath, filename)# os.path.abspath(dirpath), filename)
				#old = os.path.normpath(
				#print(old_name)
				if not os.path.exists(final_path):
					os.mkdir(final_path)
				outdir = final_path#+"/"+code+'_'+str(index[0]+1)
				if not os.path.exists(outdir):
					os.mkdir(outdir)
				csvfile =  str(uuid.uuid4()) + ".csv"#sheet+'.csv'
				fullname = os.path.normpath(os.path.join(outdir, csvfile))

				print (fullname)
				shutil.copy(old_name, fullname)
				print ("done")
			break
		
	def copy_file_in_one(self):
		mainPath = os.getcwd()
		downloadFilepath = os.path.normpath(mainPath+downloadFileFolder)
		#f = []
		df = pd.DataFrame()
		for (dirpath, dirnames, filenames) in os.walk(downloadFilepath):
			#f.extend(filenames)
			for filename in filenames:
				index = [i for i, s in enumerate(routes) if s in filename]
				print ("route number" + repr(index))

				old_name = os.path.join(dirpath, filename)# os.path.abspath(dirpath), filename)
				#old = os.path.normpath(
				print(dirpath)
				df_temp = pd.read_csv(old_name, encoding='utf-8-sig',engine='python')

				df = df.append(df_temp, ignore_index=True)

				os.remove(os.path.join(dirpath, filename))
				
			break
		if not os.path.exists(final_path):
			os.mkdir(final_path)
		outdir=final_path
		#outdir = final_path+"/"+code+'_'+str(index[0]+1)
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		csvfile =  str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		fullname = os.path.normpath(os.path.join(outdir, csvfile))

		print (fullname)
		df.rename(columns={'Value':'car_speed','Timestamp':'DateTime','Name':'path_name','PathID':'path_id'},inplace=True)
		try:
			df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d%H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+02')
		except:
			df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d').dt.strftime('%Y-%m-%dT00:00+02')
		df.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False)#headers=false

		#shutil.copy(old_name, fullname)
		print ("done")

	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP'], api_version=(2, 2, 1))
		topic = "THESS_ENV_IMET_SPEED_15MIN_SCHEDULED_DATA_INGESTION"
		producer.send(topic, b'Thessaloniki car speed scheduled data ingested to HDFS').get(timeout=30)

if __name__ == '__main__':
	a = thess_env_imet_speed_15min_batch(origin_url)
	d= a.get_session()
	if (d):
		#get the info files to the temp folder
		a.get_info()
		#end the Selenium browser session
		#d.close()
		#d.quit()
		#copy files from temp folder
		a.copy_file_in_one()
		a.producer()
		d.close()
		d.quit()






