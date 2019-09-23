# -*- coding: utf-8 -*-

"""
Downloads environmental values from 2007 until  the day before to current day. 
@version 1.3 Changes in the webpage 
"""
"""
Values are in html tables obtained after interacting with a form. 
To get the described table, URL is: http://www.havaizleme.gov.tr/STN/STN_Report/StationDataDownload
Form values are:
 nothing - nothing - antalya - 0107000 and 0107001 
 - Hava Sicakligi(°C),Hava Basinci(mbar),Ruzgar Hizi(m/s), Ruzgar Yönü(Derece),PM10(µg/m³),SO2(µg/m³) -  dates From yesterday to yesterday

Stations in Antalya: 
It shows two: 0107000 and 0107001
But 0107001 does not return any value. 
So we just check 0107000: Antalya, station 1 (36.887500, 30.726667) -> Data from use_data_catalogue_Turkey_v3

Parameters:
Hava Sicakligi(°C),Hava Basinci(mbar),Ruzgar Hizi(m/s), Ruzgar Yönü(Derece),PM10(µg/m³),SO2(µg/m³)
Air Temperature (° C), Air Pressure (mbar), Wind Speed ​​(m / s), Wind Direction (Degrees), PM10 (µg/m³), ​​SO2(µg/m³)

 Form dates: 
 <input type="hidden" name="start_TimeStamp" value="1167602400000"> 01012007
 <input type="hidden" name="end_TimeStamp" value="xxxxxxxxxxx"> yesterdays timestamp

 Wind Speed in m/s is transformed to knots  as m/s = 1.943844 knots
"""
""" data public (Ministry of Environment and Urbanism)"""
"""
	code : antalya_env_cityofantalya_perminute
	code : antalya_env_cityofantalya_perminute_1
"""
""" NOTE: if Local is set to False, the browser runs in headless mode"""
""" NOTE: path_to_webdriver_c should hold the actual path to chrome webdriver """

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import os
import uuid
import time
from datetime import timedelta, date
from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

logging.basicConfig(level=logging.INFO)
origin_url = 'http://www.havaizleme.gov.tr/STN/STN_Report/StationDataDownload'
code = 'test_antalya_env_cityofantalya_perminute'

path_to_webdriver_c = path_to_chrome_webdriver
params=['HavaSicakligi','HavaBasinc','RuzgarHizi', 'RuzgarYon','PM10','SO2'] 

l_final_path = './data/'



WINDOW_SIZE = "1920,1080"



class wait_for_display(object):
	"""class to define a WebdriverWait that waits for the change in  the css property display"""
   
	def __init__(self, locator):
		self.locator = locator

	def __call__(self, driver):
		try:
			element = EC._find_element(driver, self.locator)
			return element.value_of_css_property("display") == "block"
		except StaleElementReferenceException:
			return False


class antalya_env_cityofantalya_perminute (object):
	
	def __init__(self, url):
		self.url = url
		self.local = False
		self.file_to_move =''
		self.names =[]

	def get_session(self):
		"""Initialize webdriver and target URL, depending on environment"""
		#try: 
		if self.local:
			#CHROME
			
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c)#,chrome_options=chrome_options)
			self.driver.get(self.url)
			self.driver.implicitly_wait(60)
			self.driver.maximize_window()
			#self.driver.implicitly_wait(30)
			self.driver.get(self.url)
			

		else:
			
			#CHROME
			chrome_options = Options()  
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
			self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c,chrome_options=chrome_options)#,chrome_options=chrome_options)
			
			self.driver.get(self.url)
			self.driver.implicitly_wait(60)
			#self.driver.maximize_window()
			#self.driver.implicitly_wait(30)
			self.driver.get(self.url)#self.verificationErrors = []
			#self.accept_next_alert = True

		return self.driver
		#except:
		#	print(sys.exc_info()[0],"occured.")
		#	return False

	def select_city(self):
		
		#el1 = self.driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[1]/div[3]/div/div/span/span/span[2]')
		#Note: they changed the elements in the page
		el1 = self.driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[1]/div[2]/div/div/span/span/span[2]')

		
		el1.click()
		time.sleep(4)
		WebDriverWait(self.driver, 20).until(wait_for_display((By.XPATH, '//*[@id="CityId-list"]')))
		el = self.driver.find_element_by_xpath("""//ul[@id='CityId_listbox']/li[text()='Antalya']""")#('//*[@id="CityId_listbox"]/li[9]')#('//ul[@id = "CityId_listbox"]/li[contains(.,"Antalya")]')#('//*[@id="CityId_listbox"]/li[8]')#('//ul[@id = "CityId_listbox"]/li[contains(.,"Ankara")]')
		#el = self.driver.find_element_by_xpath("""//ul[@id='CityId_listbox']/li/font/font[text()='Adana']""")
		#el = self.driver.find_element_by_xpath("""//*[@id="CityId_listbox"]/li[8]""")
		actions = ActionChains(self.driver)
		actions.move_to_element(el)
		actions.pause(1)
		actions.click()#send_keys('A')
		actions.perform()


	def fill_form(self):
		#city
		#<ul unselectable="on" class="k-list k-reset" tabindex="-1" aria-hidden="false" id="CityId_listbox" aria-live="polite" data-role="staticlist" role="listbox">
		#<li tabindex="-1" role="option" unselectable="on" class="k-item" data-offset-index="6">Ankara</li></ul>
		#

		print ("el1")
		self.select_city()

		el11 = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('id11 '+el11.get_attribute("id"))
		print ('class11 '+el11.get_attribute("class"))
		
		#SELECT STATIONS
		print ("stations dropdown open")
		print ("el2")		
		el2 = self.driver.find_element_by_xpath("""//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[1]/div[4]/div/div/div/div""")#//div[@class='k-multiselect-wrap k-floatwrap']

		actions = ActionChains(self.driver)
		actions.move_to_element(el2)
		actions.pause(3)
		actions.click(el2)
		actions.perform()

		el22 = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('id22 '+el22.get_attribute("id"))
		print ('class22 '+el22.get_attribute("class"))

		
		#click stations dropdown
		print ("stations dropdown")

		wait = WebDriverWait(self.driver, 10)

		#Changed
		try:
			element = wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@id='StationIds-list']//ul[@id='StationIds_listbox']/li[text()='0107000 Antalya- (Antalya-Muratpaşa)']"),'Antalya'))
		except Exception as e:
			print(e)
			self.select_city()
			wait = WebDriverWait(self.driver, 20)
			element = wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@id='StationIds-list']//ul[@id='StationIds_listbox']/li[text()='0107000 Antalya- (Antalya-Muratpaşa)'"),'Antalya'))


		#to click all the stations use this code
		"""
		stitems = self.driver.find_elements_by_xpath("//div[@id='StationId-list']//ul[@id='StationId_listbox']/li")
		
		for item in stitems:
			try:
				if 'Antalya' in item.text:
				#	print ('item '+item.text+ " : "+item.get_attribute("class"))
					print ('aqui')
					actions = ActionChains(self.driver)
					actions.move_to_element(item)
					#actions.pause(1)
					actions.click(item)
					actions.perform()
			except Exception as e:
				print(e)
		"""
		#at this moment, just one station is giving values, so just click that one
		
		#XPATH: to div where the list of stations; THIS has changed 
			
		sitem = self.driver.find_element_by_xpath("//div[@id='StationIds-list']//ul[@id='StationIds_listbox']/li[text()='0107000 Antalya- (Antalya-Muratpaşa)']")
		actions = ActionChains(self.driver)
		actions.move_to_element(sitem)
		actions.pause(1)
		actions.click(sitem)
		actions.perform()
		self.names.append(sitem.text)
		
		#print ('item1 '+liitems_1.text+ " : "+liitems_1.get_attribute("class"))
		#liitems_2 = self.driver.find_element_by_xpath("//div[@id='StationId-list']//ul[@id='StationId_listbox']/li[2]")
		#print ('item1 '+liitems_2.text+ " : "+liitems_2.get_attribute("class"))
		el33 = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('id33 '+el33.get_attribute("id"))
		print ('class33 '+el33.get_attribute("class"))
		time.sleep(5)
		#in case the dropdown does not hide. PROBLEM: focus goes to body
		#self.driver.execute_script("document.getElementById('StationIds-list').style.display = 'none';")
		#time.sleep(5)


		#SELECT HOUR
		#XPATH //*[@id="StationDataDownloadForm"]/fieldset[1]/div[2]/div[1]/div/div/span/span
		#OLD XPATH: //*[@id='page-wrapper']/div[2]/form/fieldset[1]/div[2]/div[4]/div/div/span[1]/span
		print ("hours dropdown")		
		el5 = self.driver.find_element_by_xpath("""//*[@id='page-wrapper']/div[2]/form/fieldset[1]/div[2]/div[1]/div/div/span/span""")#//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[2]/div[4]/div/div/span/span/span[2]""")
		actions = ActionChains(self.driver)
		actions.move_to_element(el5)
		actions.pause(3)
		actions.click(el5)
		actions.perform()

		el55 = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('id55 '+el55.get_attribute("id"))
		print ('class55 '+el55.get_attribute("class"))

		
		#WebDriverWait(self.driver, 30).until(wait_for_display((By.XPATH, '//body/div[11]')))
		WebDriverWait(self.driver, 30).until(wait_for_display((By.XPATH, """//*[@id="TimeUnit-list"]""")))

		houritem = self.driver.find_element_by_xpath("""//ul[@id='TimeUnit_listbox']/li[text()='1 Saat']""")

		#for item in paritems:

			#try:
				#print ('item '+item.text)
		if houritem.text is '1 Saat':
		#	print ('item '+item.text+ " : "+item.get_attribute("class"))
			print ('hour ')
		else:
			houritem = self.driver.find_element_by_xpath("""//div[@id='TimeUnit-list']//ul[@id='TimeUnit_listbox']/li[1]""")

		actions = ActionChains(self.driver)
		actions.move_to_element(houritem)
		actions.pause(2)
		actions.click(houritem)
		actions.perform()
			#		break
			#except Exception as e:
			#	print(e)



		#SELECT PARAMETERS
		#Click on parameters dropdown
		print ("parameters dropdown open")
		#XPATH: to div where the list of parameters; THIS has changed 		
		#OLDel4 = self.driver.find_element_by_xpath("""//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[2]/div[1]/div/div/div""")#//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[1]/div[4]/div/div/div/div')
		
		param_dd = self.driver.find_element_by_xpath("""//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[2]/div[4]/div/div/div/div""")#//*[@id="StationDataDownloadForm"]/fieldset[1]/div[2]/div[4]/div/div/div/div""")

		print ('idparam_dd'+param_dd.get_attribute("id"))
		print ('classparam_dd '+param_dd.get_attribute("class"))

		actions = ActionChains(self.driver)
		actions.move_to_element(param_dd)
		actions.pause(3)
		actions.click(param_dd)
		actions.perform()

		el44 = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('id44 '+el44.get_attribute("id"))
		print ('class44 '+el44.get_attribute("class"))

		#
		#To check element by element (not working everytime)
		"""
		paritems = self.driver.find_elements_by_xpath("//div[@id='SelectedParameters-list']//ul[@id='SelectedParameters_listbox']/li")
		i=0
		for item in paritems:
			try:
				#print ('item '+item.text)
				if item.text in params:
					print ('item '+item.text)#+ " : "+item.get_attribute("class"))
					print ('param ' +str(i))
					actions = ActionChains(self.driver)
					actions.move_to_element(item)
					actions.pause(3)
					actions.click(item)
					actions.perform()
					i+=1
			except Exception as e:
				print(e)
		"""
		#XPATH: to div where the list of parameters; THIS has changed 	
		#OLD: //div[@id='SelectedParameters-list']//ul[@id='SelectedParameters_listbox']/li[text()='PM10']
		paritem = self.driver.find_element_by_xpath("""//div[@id='Parameters-list']//ul[@id='Parameters_listbox']/li[text()='PM10']""")#li[1]")
		actions = ActionChains(self.driver)
		actions.move_to_element(paritem)
		actions.pause(3)
		actions.click(paritem)
		actions.perform()

		paritem = self.driver.find_element_by_xpath("""//div[@id='Parameters-list']//ul[@id='Parameters_listbox']/li[text()='SO2']""")#li[2]")
		actions = ActionChains(self.driver)
		actions.move_to_element(paritem)
		actions.pause(3)
		actions.click(paritem)
		actions.perform()

		paritem = self.driver.find_element_by_xpath("""//div[@id='Parameters-list']//ul[@id='Parameters_listbox']/li[text()='Hava Basinci']""")#li[19]")
		actions = ActionChains(self.driver)
		actions.move_to_element(paritem)
		actions.pause(3)
		actions.click(paritem)
		actions.perform()

		paritem = self.driver.find_element_by_xpath("""//div[@id='Parameters-list']//ul[@id='Parameters_listbox']/li[text()='Hava Sicakligi']""")#li[20]")
		actions = ActionChains(self.driver)
		actions.move_to_element(paritem)
		actions.pause(3)
		actions.click(paritem)
		actions.perform()

		paritem = self.driver.find_element_by_xpath("""//div[@id='Parameters-list']//ul[@id='Parameters_listbox']/li[text()='Ruzgar Hizi']""")#li[39]")
		actions = ActionChains(self.driver)
		actions.move_to_element(paritem)
		actions.pause(3)
		actions.click(paritem)
		actions.perform()

		paritem = self.driver.find_element_by_xpath("""//div[@id='Parameters-list']//ul[@id='Parameters_listbox']/li[text()='Ruzgar Yönü']""")#li[40]")
		actions = ActionChains(self.driver)
		actions.move_to_element(paritem)
		actions.pause(3)
		actions.click(paritem)
		actions.perform()



		#SEST START DATE AND END DATE
		#print(datetime.date.today().timestamp())
		"""
		now = datetime.datetime.now().replace(hour=0, minute=0,second=0)
		day =now.strftime("%Y-%m-%d")
		print(now.strftime("%Y-%m-%d %H:%M:%S"))
		print(now.timestamp())
		b = int(now.timestamp()) * 1000
		print (b)
		date = datetime.datetime.fromtimestamp(1543356000000 / 1e3)
		print (date)
		"""

		"""yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
		DAY = 24*60*60 # POSIX day in seconds
		timestamp = (yesterday.toordinal() - date(1970, 1, 1).toordinal()) * DAY
		print (timestamp)
		"""
		yesterday = datetime.datetime.now() - timedelta(days=1)#now() returns the current time in UTC
		yesterday.strftime('%m%d%y')
		yesterdayDate = yesterday.strftime("%Y-%m-%d")
		yesterdayts = int(yesterday.timestamp()) * 1000
		print (yesterdayts)

		datet = datetime.datetime.fromtimestamp(yesterdayts / 1e3)
		print (datet)
		
		ts01012007 = 1167602400000 #timestap for first day of 2007

		"""first date <input type="hidden" name="start_TimeStamp" value="1167602400000"> """
		self.driver.execute_script("document.getElementsByName('start_TimeStamp')[0].value='"+str(ts01012007)+"'")
		"""last date  <input type="hidden" name="end_TimeStamp" value="1543356000000">"""
		self.driver.execute_script("document.getElementsByName('end_TimeStamp')[0].value='"+str(yesterdayts)+"'")
		"""value: datetime.date.today().timestamp() """
		#print(datetime.date.today().timestamp())


		#SELECT HOUR <-- JUST REPEAT FOR BEING ABLE TO CLICK THE BUTTON (the properties dropdown hides it and clicking to close change focus to body)
		#XPATH //*[@id="StationDataDownloadForm"]/fieldset[1]/div[2]/div[1]/div/div/span/span
		#OLD XPATH: //*[@id='page-wrapper']/div[2]/form/fieldset[1]/div[2]/div[4]/div/div/span[1]/span
		print ("hours dropdown")		
		el5 = self.driver.find_element_by_xpath("""//*[@id='page-wrapper']/div[2]/form/fieldset[1]/div[2]/div[1]/div/div/span/span""")#//*[@id="page-wrapper"]/div[2]/form/fieldset[1]/div[2]/div[4]/div/div/span/span/span[2]""")
		actions = ActionChains(self.driver)
		actions.move_to_element(el5)
		actions.pause(3)
		actions.click(el5)
		actions.perform()

		el55 = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('id55 '+el55.get_attribute("id"))
		print ('class55 '+el55.get_attribute("class"))

		
		#WebDriverWait(self.driver, 30).until(wait_for_display((By.XPATH, '//body/div[11]')))
		WebDriverWait(self.driver, 30).until(wait_for_display((By.XPATH, """//*[@id="TimeUnit-list"]""")))

		houritem = self.driver.find_element_by_xpath("""//ul[@id='TimeUnit_listbox']/li[text()='1 Saat']""")

		#for item in paritems:

			#try:
				#print ('item '+item.text)
		if houritem.text is '1 Saat':
		#	print ('item '+item.text+ " : "+item.get_attribute("class"))
			print ('hour ')
		else:
			houritem = self.driver.find_element_by_xpath("""//div[@id='TimeUnit-list']//ul[@id='TimeUnit_listbox']/li[1]""")

		actions = ActionChains(self.driver)
		actions.move_to_element(houritem)
		actions.pause(2)
		actions.click(houritem)
		actions.perform()
			#		break
			#except Exception as e:
			#	print(e)





		""" Button"""
		print ("button")
		button = self.driver.find_element_by_xpath("""//button[text()='Sorgula']""")
		#button.click()
		actions = ActionChains(self.driver)
		actions.move_to_element(button).click(button)
		actions.perform()

		elbut = self.driver.switch_to.active_element#self.driver.find_element_by_xpath('//*[@id="CityId-list"]/span/input')
		print ('idbut '+elbut.get_attribute("id"))
		print ('classbut '+elbut.get_attribute("class"))

		time.sleep(5)

		notdone = True
		i=0
		wait = WebDriverWait(self.driver, 10)
		while notdone:
		
			try:
				element = wait.until(EC.presence_of_element_located((By.XPATH,"""//*[@id="grid"]/div[1]/a""")))
				notdone = False
			except:
				if (i<20):
					i+=1
				else:
					print ('info took too long to load; not today')
					notdone = False
		
		#To download excel click on: //*[@id="grid"]/div[1]/a"""
		"""
		print ("excel")
		excel = self.driver.find_element_by_xpath(" ""//*[@id="grid"]/div[1]/a"" "")
		actions = ActionChains(self.driver)
		actions.move_to_element(excel).click(excel)
		actions.perform()
		"""
		
		#Scroll to the end to be able to press  "show all results"
		html = self.driver.find_element_by_tag_name('html')
		html.send_keys(Keys.END)
		print ("showall")
		#Show all drop down
		## OPEN DROPDOWN
		#XPath //*[@id="grid"]/div[5]/span[1]/span/span
		# (OLD XPATH //*[@id="grid"]/div[4]/span[1]/span/span/span[2]/span
		showalldrop = self.driver.find_element_by_xpath("""//*[@id="grid"]/div[5]/span[1]/span/span""")
		
		actions = ActionChains(self.driver)
		actions.move_to_element(showalldrop).click(showalldrop)
		actions.perform()

		#To show all option click on :	 
		#OLD XPATH	/html/body/div[11]/div/div[2]/ul/li[1]
		#XPATH: //body/div[11]/div/div[2]/ul/li[4]
		showall = self.driver.find_element_by_xpath("""//body/div[11]/div/div[2]/ul/li[4]""")
		actions = ActionChains(self.driver)
		actions.move_to_element(showall)
		actions.pause(3)
		actions.click(showall)
		actions.perform()

		#Now CLICK refresh
		#XPATH //*[@id="grid"]/div[5]/a[5]
		
		print ("refresh")
		refresh = self.driver.find_element_by_xpath("""//*[@id="grid"]/div[5]/a[5]""")
		actions = ActionChains(self.driver)
		actions.move_to_element(refresh)
		actions.pause(3)
		actions.click(refresh)
		actions.perform()


		time.sleep(5)

		#Parse the tables
		soup_level2=BeautifulSoup(self.driver.page_source, 'lxml')

		tables = soup_level2.find_all('table')

		headers_table = tables[5]#0
		times_table = tables[6]
		values_table = tables[7]#1

		df_headers = pd.read_html(str(headers_table),header=[0,1])
		#print (df_headers[0].columns.tolist)
		hnames =df_headers[0].columns.get_level_values(level=1)

		df_values = pd.read_html(str(values_table),header=None,decimal=',',thousands='.')
		df_times = pd.read_html(str(times_table),header=None)
		print (df_values[0].columns.tolist)
		print (df_times[0].columns.tolist)
		values = df_values[0]
		#Change columns names
		#values.columns = ["DateTime", hnames[0], hnames[1],hnames[2],hnames[3],hnames[4],hnames[5]]
		values.columns = [hnames[0], hnames[1],hnames[2],hnames[3],hnames[4],hnames[5]]
		values["DateTime"] = df_times[0]
		values["DateTime"]= values["DateTime"].astype(str)
		#Clean columns names
		values.columns = values.columns.str.replace(r"\(.*\)","")#remove all braces and data inside
		
		

		#translate column names
		values.rename(columns={'PM10 ':'PM10','SO2 ':'SO2','HavaSicakligi ':'air_temperature','HavaBasinc ':'air_preassure','RuzgarHizi ':'wind_speed_ms', 'RuzgarYon ':'wind_from_direction'},inplace=True)

		#oldvalues.rename(columns={'Hava Sicakligi':'air_temperature','Hava Basinci':'air_preassure','Ruzgar Hizi':'wind_speed_ms', 'Ruzgar Yönü':'wind_from_direction'},inplace=True)

		#reformat date
		values['DateTime'] = pd.to_datetime(values['DateTime'], format='%d.%m.%Y %H:%M').dt.strftime('%Y-%m-%dT%H:%M+03')
		
		#add necessary columns
		values['station_id'] = self.names [0]
		values['Latitude'] = 36.887500
		values['Longitude'] = 30.726667
		try:
			#values['wind_speed'] = 1.943844 * values['wind_speed_ms'].astype(float)
			values['wind_speed'] = 1.943844 *pd.to_numeric(values['wind_speed_ms'], errors='coerce')
		except:
			print ('Cannot transform to knots')

		print(values.dtypes)

		df_final = pd.DataFrame()
		df_final = df_final.append(values, ignore_index=True)

		
		#create file
		touterdir = l_final_path
		if not os.path.exists(touterdir):
			os.mkdir(touterdir)
		toutdir = touterdir + code
		if not os.path.exists(toutdir):
			os.mkdir(toutdir)
		#no subindex folder
		#ttoutdir = toutdir +'/'+ code+'_1'
		#if not os.path.exists(ttoutdir):
		#	os.mkdir(ttoutdir)
		csvfile =  str(uuid.uuid4()) + ".csv"
		tfilename = os.path.join(toutdir, csvfile)#change to ttoutdir if subindex folder

		#copy to
		#fpath = l_final_path+code+'/'
		#filname = fpath + csvfile

		#create the file with just new values
		df_final.to_csv(tfilename, mode='w', encoding='utf-8-sig', index=False)
	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['10.10.2.51:9092'], api_version=(2, 2, 1))
		topic = "ANTALYA_ENV_CITYOFANTALYA_PERMINUTE_DATA_INGESTION"
		producer.send(topic, b'City of antalya perminute environmental data ingested to HDFS').get(timeout=30)

if __name__ == '__main__':
	a = antalya_env_cityofantalya_perminute(origin_url)
	d= a.get_session()
	if (d):
		a.fill_form()
		#end the Selenium browser session
		d.close()
		d.quit()