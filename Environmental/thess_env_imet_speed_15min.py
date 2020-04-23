# -*- coding utf-8 -*-
"""
https://www.trafficthessreports.imet.gr/user_login.aspx
NOTE: when opening with https://www.trafficthessreports.imet.gr/export.aspx:
---> shows login page BUT redirects to desired page


Login and password should be in an .env file as
TRAFFIC_EMAIL=email_account
TRAFFIC_PASSWORD=password

login form:
-input name="Login1$UserName" id ="Login1_UserName"
-input name ="Login1$Password" id="Login1_Password"

-input name="Login1$LoginButton" id="Login1_LoginButton"

Routes:
1. Εγνατία (Συντριβάνι - Πλατεία Δημοκρατίας)
2. Εγνατία (Πλατεία Δημοκρατίας - Συντριβάνι)
8. Δραγούμη
9. Βενιζέλου.

This crawler is for collecting data every increment (default = 15) minutes: from 15 minutes ago to current time.

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
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from urllib.request import urlopen, urlretrieve

import re
import pandas as pd
import datetime
import os
import shutil
import uuid
import time
from datetime import timedelta, date

from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

#log_file_path = '../../logger.log'

logging.basicConfig(level=logging.INFO)

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


basic_url = 'https://www.trafficthessreports.imet.gr'
origin_url = basic_url+'/export.aspx'

code = 'thess_env_imet_speed_15min'

#path_to_webdriver_c = path_to_Chrome_webdriver


#where the files are temporaly downloaded
downloadFileFolder = '/home/oulu/THESS/data/environmental/temp/thess_env_imet_speed_15min/'
l_final_path = '/home/oulu/THESS/data/environmental/thess_env_imet_speed_15min/'
final_path = '/home/oulu/THESS/data/environmental/thess_env_imet_speed_15min/'

routes = ["1. Εγνατία (Συντριβάνι - Πλατεία Δημοκρατίας)","2. Εγνατία (Πλατεία Δημοκρατίας - Συντριβάνι)","8. Δραγούμη","9. Βενιζέλου"]
routesNr= [1,2,8,9]
WINDOW_SIZE = "1920,1080"

startTime =""
endTime =""
startDate =""
endDate =""
increment = 15


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
    self.numbers = []
    self.downloadDir =""
    load_dotenv()


  def enable_download_headless(self,download_dir):
    self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    self.driver.execute("send_command", params)
  def get_session(self):
    mainPath = os.getcwd()
    downloadFilepath = os.path.normpath(downloadFileFolder)
    self.downloadDir = downloadFilepath
    if self.local:
      chrome_options = Options()
      #os.makedirs(downloadFilepath)
      mainPath = os.getcwd()
      downloadFilepath = os.path.normpath(downloadFileFolder)
      print(downloadFilepath+"yoo")
      preferences = {"profile.default_content_settings.popups": 0,'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory": downloadFilepath ,"download.prompt_for_download": False }#,"directory_upgrade": True,"safebrowsing.enabled": True }
      chrome_options.add_experimental_option("prefs", preferences)
      self.driver = webdriver.Chrome(executable_path='/home/oulu/usr/chromedriver.exe',chrome_options=chrome_options)
      str1 = ''
      if 'browserVersion' in self.driver.capabilities:
        str1= self.driver.capabilities['browserVersion']
      else:
        str1= self.driver.capabilities['version']
        str2 = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
      print(str1)
      print(str2)
      print(str1[0:2])
      print(str2[0:2])
      if str1[0:2] != str2[0:2]:
        print("please download correct chromedriver version")
    else:
      chrome_options = Options()
      chrome_options.add_argument("--headless")
      chrome_options.add_argument("--window-size=1920x1080")
      chrome_options.add_argument("--disable-notifications")
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--verbose')
      #chrome_options.add_argument('--remote-debugging-port=9222')
      chrome_options.add_experimental_option("prefs", {"download.default_directory": downloadFilepath,"download.prompt_for_download":False, "download.directory_upgrade": True,"safebrowsing_for_trusted_sources_enabled": False,"safebrowsing.enabled": False})
      chrome_options.add_argument('--disable-gpu')
      #chrome_options.add_argument('--disable-software-rasterizer')
      # initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
      self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',options=chrome_options)
      # change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
      download_dir = downloadFilepath
      # function to handle setting up headless download
      self.enable_download_headless(download_dir)
      self.driver.get(self.url)
      self.driver.implicitly_wait(60)
      #self.driver.maximize_window()
      #self.driver.implicitly_wait(30)
      self.driver.get(self.url)
      return self.driver
      #except:
      #print(sys.exc_info()[0],"occured.")
      #returnFalse
  def fill_login(self):
    """
    Fill the login''
    id ="Login1_UserName"
    id="Login1_Password"
    """
    #TRAFFIC_KEY = os.getenv("TRAFFIC_EMAIL")
    #TRAFFIC_PASSWORD = os.getenv("TRAFFIC_PASSWORD")
    self.driver.find_element_by_id("Login1_UserName").send_keys('YOUR_USER')
    self.driver.find_element_by_id("Login1_Password").send_keys('YOUR_PASSWORD')

    self.driver.find_element_by_id("Login1_LoginButton").click()

  def get_info(self):
    """
    id ="ExportDropDownList"
    """
    try:
      self.fill_login()
    except Exception as e:
      self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source format is not as expected',e)
      return False

    try:
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
          except UnexpectedAlertPresentException as e:
            print ('alert')
            alert = self.driver.switch_to.alert
            alert.accept()
            wait2 = WebDriverWait(self.driver, 15)
            notdone = False

            break
          except:
            if (i<10):
              notdone= True
              i+=1
              print (i)
            else:
              print ('info took too long to load; not today')
              notdone = False
              break
        notdone = True

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
        minbefore= now - datetime.timedelta(minutes=increment)

        startDate= minbefore.strftime("%d-%m-%Y")
        startTime = minbefore.strftime("%H:%M")

        endDate =now.strftime("%d-%m-%Y")
        endTime =now.strftime("%H:%M")



        """now = datetime.datetime.now()#.replace(hour=0, minute=0,second=0)
        endDate = now.strftime("%d-%m-%Y")
        endTime = now.strftime("%H:%M")
        """

        """<input type="hidden" name="FromDateHiddenField" id="FromDateHiddenField" value="01-01-2017"> """
        self.driver.execute_script("document.getElementById('FromDateHiddenField').value='"+startDate+"'")
        """<input type="hidden" name="FromTimeHiddenField" id="FromTimeHiddenField" value="00:56">"""
        self.driver.execute_script("document.getElementById('FromTimeHiddenField').value='"+startTime+"'")
        """<input type="hidden" name="ToDateHiddenField" id="ToDateHiddenField" value="26-02-2019"> """
        self.driver.execute_script("document.getElementById('ToDateHiddenField').value='"+endDate+"'")
        """<input type="hidden" name="ToTimeHiddenField" id="ToTimeHiddenField" value="09:50">"""
        self.driver.execute_script("document.getElementById('ToTimeHiddenField').value='"+endTime+"'")

        time.sleep(5)
        print('dates done')

        #this cancels the bindHiddenFields() function. That funtion would substitute the data we have written in the hidden
        #fields with the default ones
        self.driver.execute_script("bindHiddenFields = function bindHiddenFields() { return true;}")


        """ Button: Press to ask for the file"""
        print ("button ask file")
        button = self.driver.find_element_by_xpath("""//*[@id="ExportButton"]""")

        #button.click()
        actions = ActionChains(self.driver)
        actions.move_to_element(button).click(button)
        actions.perform()

        ''' Wait for & get Result '''

        time.sleep(5)
        print ("wait for download button ")
        notdone = True
        i=0
        wait = WebDriverWait(self.driver, 20)
        while notdone:

          try:
            element = wait.until(EC.presence_of_element_located((By.XPATH,"""//*[@id="UpdatePanel1"]/a[2]""")))
            notdone = False
          except UnexpectedAlertPresentException as e:
            print ('alert in update')
            try:
              alert = self.driver.switch_to.alert
              alert.accept()
            except:
              print ('e in close alert')
            notdone = False
            break
          except:
            if (i<6):
              notdone = True
              i+=1
            else:
              print ('info took too long to load; not today')
              notdone = False

        wait2 = WebDriverWait(self.driver, 15)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        anchor =None
        try:
          anchor = self.driver.find_element_by_xpath("""//*[@id="UpdatePanel1"]/a[2]""")
          anchor.click()
          print ("click ")
          time.sleep(30)
          print ("check if files in temp dir")
          print (self.downloadDir)
          #Check if file downloaded, extra for headless mode
          for (dirpath, dirnames, filenames) in os.walk(self.downloadDir):

            if not any(routeName in s for s in filenames):
              try:
                print ("file not downloaded with click")

                href = anchor.get_attribute("href")
                print (href)
                filename = routeName #href.rsplit('/', 1)[-1]
                fullname = os.path.join(self.downloadDir, filename)
                try:
                  urlretrieve(href, fullname)
                  print ("downloaded url retrieve")
                except Exception as e:
                  print ('file not downloaded with url retrieve')
                  print (e)
              except Exception as e:
                print ('problems with  url retrieve')
                print (e)
            else:
              print ("file downloaded with click")

        except:
          print ("no button")

    except Exception as e:
      print ("here1 ")
      print (e)
      self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source format is not as expected',e)
      return False

    print ("Done downloading new data")
    return True

  def copy_file_in_one(self):
    print('copy file in one')
    mainPath = os.getcwd()
    downloadFilepath = os.path.normpath(downloadFileFolder)
    #f = []
    print(downloadFilepath)
    df = pd.DataFrame()
    haveFiles=False
    try:
      for (dirpath, dirnames, filenames) in os.walk(downloadFilepath):
        #f.extend(filenames)
        print('for in')
        haveFiles=False
        for filename in filenames:
          print('filename')
          #print(filename)
          index = [i for i, s in enumerate(routes) if s in filename]
          print ("route number" + repr(index))

          old_name = os.path.join(dirpath, filename)# os.path.abspath(dirpath), filename)
          #old = os.path.normpath(
          print(dirpath)
          print('read downloaded csv')
          df_temp = pd.read_csv(old_name, encoding='utf-8-sig',engine='python')
          print('append to df')
          df = df.append(df_temp, ignore_index=True)
          haveFiles = True
          os.remove(os.path.join(dirpath, filename))

        break
    except Exception as e:
      print(e)
      self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source not found or cannot be open',e)
      return False

    if haveFiles:
      try:
        print('create csv file')
        if not os.path.exists(final_path):
          os.mkdir(final_path)
        outdir=final_path
        #outdir = final_path+"/"+code+'_'+str(index[0]+1)
        if not os.path.exists(outdir):
          os.mkdir(outdir)
        csvfile =  str(uuid.uuid4()) + ".csv"#sheet+'.csv'
        fullname = os.path.normpath(os.path.join(outdir, csvfile))

        print (fullname)

      except Exception as e:
        self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'cannot create folder/file to store data',e)
        return False

      try:
        print('renaming columns')
        df.rename(columns={'Value':'car_speed','Timestamp':'DateTime','Name':'path_name','PathID':'path_id'},inplace=True)
        print('DateTime format')
        try:
          df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+02')
        except:
          df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d').dt.strftime('%Y-%m-%dT00:00+02')

      except Exception as e:
        print (e)
        self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source format is not as expected',e)
        return False
      try:
        df.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False)#headers=false
      except Exception as e:
        self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'cannot store data in file',e)
        return False

      #shutil.copy(old_name, fullname)
      print ("done")
      return True
    else:
      print('no files downloaded')
      self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source not found or cannot be open')
      return False


  def producer(self,topic,msg,e=None):
    """ This function sends data to kafka bus"""
    producer = KafkaProducer(bootstrap_servers=['HOST_IP', 'HOST_IP', 'HOST_IP']
                          ,security_protocol='SSL',
                          ssl_check_hostname=True,
                          ssl_cafile='/home/oulu/certs/ca-cert',
                          ssl_certfile='/home/oulu/certs/cutler-p3-c1-00.crt',
                          ssl_keyfile='/home/oulu/certs/cutler-p3-c1-00.key')
    msg_b = str.encode(msg)
    producer.send(topic, msg_b).get(timeout=30)
    if (e):
      logging.exception('exception happened')



if __name__ == '__main__':
  a = thess_env_imet_speed_15min_batch(origin_url)
  try:
    d= a.get_session()


    if (d):
      #get the info files to the temp folder
      if (a.get_info()):
        #copy files from temp folder
        if(a.copy_file_in_one()):
          a.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_INGESTION",'IMET VEHICLE SPEED data ingested to HDFS')
      #end the Selenium browser session
      d.close()
      d.quit()

  except Exception as e:
    print(e)
    a.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source not found or cannot be open',e)
