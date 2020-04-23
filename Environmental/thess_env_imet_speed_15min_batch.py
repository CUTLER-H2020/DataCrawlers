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

This crawler is for batch data. It will query for data from
2017
2018
2019 up to day before today
The data collection is splitted into several date groups because downloading the whole batch fails

NOTE: self.local = True, if browser can be open. Set to False if no browser window should be open (run in headless mode)

NOTE: Η χρονική περίοδος για την εξαγωγή των δεδομένων δεν μπορεί να υπερβαίνει τις 90 μέρες (έχετε επιλέξει 248)
The time period for exporting data cannot exceed 90 days (you have selected 248)

NOTE @update December 2019: page only allows intervals of maximum 90 days
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
#from bs4 import BeautifulSoup
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
path_to_webdriver_c ='/usr/bin/chromedriver'

#where the files are temporaly downloaded

downloadFileFolder = '/home/oulu/THESS/data/environmental/temp/thess_env_imet_speed_15min_batch/'
final_path = '/home/oulu/THESS/data/environmental/thess_env_imet_speed_15min/'



WINDOW_SIZE = "1920,1080"
routes = ["1. Εγνατία (Συντριβάνι - Πλατεία Δημοκρατίας)","2. Εγνατία (Πλατεία Δημοκρατίας - Συντριβάνι)","8. Δραγούμη","9. Βενιζέλου"]

increment = 90

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
                self.downloadDir =""
                load_dotenv()

        def enable_download_headless(self,download_dir):
                self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
                params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
                self.driver.execute("send_command", params)


        def get_session(self):
                """Initialize webdriver and target URL, depending on environment"""
                #os.makedirs(downloadFilepath)
                mainPath = os.getcwd()
                downloadFilepath = os.path.normpath(downloadFileFolder)
                #downloadFilepath = os.path.normpath(mainPath+downloadFileFolder)

                print(downloadFilepath)
                self.downloadDir = downloadFilepath
                if self.local:
                        #CHROME

                        chrome_options = Options()
                        #os.makedirs(downloadFilepath)
                        preferences = {"profile.default_content_settings.popups": 0,'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory": downloadFilepath ,"download.prompt_for_download": False }#,"directory_upgrade": True,"safebrowsing.enabled": True }
                        chrome_options.add_experimental_option("prefs", preferences)
                        self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c,chrome_options=chrome_options)



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
                        self.driver = webdriver.Chrome(executable_path=path_to_webdriver_c,chrome_options=chrome_options)
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


        def fill_login(self):
                """
                Fill the login''
                id ="Login1_UserName"
                id="Login1_Password"
                """
                #TRAFFIC_KEY = os.getenv("TRAFFIC_EMAIL")
                #TRAFFIC_PASSWORD = os.getenv("TRAFFIC_PASSWORD")
                self.driver.find_element_by_id("Login1_UserName").send_keys("YOUR_EMAIL")#"cutler.oulu@gmail.com")
                self.driver.find_element_by_id("Login1_Password").send_keys("YOUR_PASSWORD")#"pass1234")
                self.driver.find_element_by_id("Login1_LoginButton").click()

        def get_info(self):
                """
                id ="ExportDropDownList"
                """

                try:
                        self.fill_login()
                except Exception as e:
                        print (e)
                        self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source format is not as expected',e)
                        return False
                #wait until correct page loaded


                try:
                        startTime ="00:00"
                        endTime ="23:59"
                        start_date1 = "01-01-2017"
                        start_date2 = "01-04-2019"

                        now = datetime.datetime.now()#.replace(hour=0, minute=0,second=0)
                        endDateToday = now.strftime("%d-%m-%Y")
                        endTimeToday = now.strftime("%H:%M")


                        routenum = 0
                        for routeName in routes:
                                print (repr(routenum))


                                #initialize dates
                                if( routenum==3):
                                        startDate= datetime.datetime.strptime(start_date2, "%d-%m-%Y")#"%m/%d/%y")
                                else:
                                        startDate= datetime.datetime.strptime(start_date1, "%d-%m-%Y")

                                endDate = startDate + datetime.timedelta(days=increment)
                                endDateTodayCompare = datetime.datetime.strptime(endDateToday, "%d-%m-%Y")

                                routenum=routenum+1
                                print (startDate)
##############################################################################################################
                                looping = True

                                while looping:
                                        if endDate > endDateTodayCompare:
                                                print('last loop')
                                                endDate = endDateTodayCompare
                                                looping = False
                                #for idx, date in enumerate(dates):
                                        print ('here1')
                                        notdone = True
                                        i=0

                                        wait = WebDriverWait(self.driver, 10)
                                        while notdone:

                                                try:
                                                        element = wait.until(EC.presence_of_element_located((By.XPATH,"""//*[@id="ExportDropDownList"]""")))
                                                        print ('here2')
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
                                        print ('here3')

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

                                        sD = startDate.strftime("%d-%m-%Y")
                                        eD = endDate.strftime("%d-%m-%Y")

                                        """<input type="hidden" name="FromDateHiddenField" id="FromDateHiddenField" value="01-01-2017"> """
                                        self.driver.execute_script("document.getElementsByName('FromDateHiddenField')[0].value='"+sD+"'")
                                        """<input type="hidden" name="FromTimeHiddenField" id="FromTimeHiddenField" value="00:56">"""
                                        self.driver.execute_script("document.getElementsByName('FromTimeHiddenField')[0].value='"+startTime+"'")
                                        """<input type="hidden" name="ToDateHiddenField" id="ToDateHiddenField" value="26-02-2019"> """
                                        self.driver.execute_script("document.getElementsByName('ToDateHiddenField')[0].value='"+eD+"'")
                                        """<input type="hidden" name="ToTimeHiddenField" id="ToTimeHiddenField" value="09:50">"""
                                        self.driver.execute_script("document.getElementsByName('ToTimeHiddenField')[0].value='"+endTime+"'")


                                        time.sleep(5)
                                        print('dates done')
                                        fromDate= self.driver.find_element_by_name('FromDateHiddenField')
                                        print(fromDate.get_attribute('value'))
                                        toDate= self.driver.find_element_by_name('ToDateHiddenField')
                                        print(toDate.get_attribute('value'))

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
                                        wait = WebDriverWait(self.driver, 10)
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

                                                if self.local:
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
                                                                                filename = routeName+'_'+sD+'_'+eD #href.rsplit('/', 1)[-1]
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

                                                else:
                                                        try:
                                                                print ("headless mode, url download")

                                                                href = anchor.get_attribute("href")
                                                                print (href)
                                                                filename = routeName+'_'+sD+'_'+eD #href.rsplit('/', 1)[-1]
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

                                        except:
                                                print ("no button")



                                        self.driver.refresh()


                                        #Update dates
                                        startDate = endDate + datetime.timedelta(days=1)
                                        endDate = startDate + datetime.timedelta(days=90)
                                ##############################################################################################################################################

                except Exception as e:
                        print (e)
                        self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source format is not as expected',e)
                        return False

                print ("Done downloading batch")
                return True


        def copy_files_in_one(self):
                print('copy file in one')
                mainPath = os.getcwd()
                downloadFilepath = os.path.normpath(downloadFileFolder)
                df = pd.DataFrame()
                haveFiles=False
                try:
                        for (dirpath, dirnames, filenames) in os.walk(downloadFilepath):
                                print('for in')
                                haveFiles=False
                                for filename in filenames:
                                        print('filename')
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
                                        #os.remove(os.path.join(dirpath, filename))

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
                                try:
                                        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+02')
                                except:
                                        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d').dt.strftime('%Y-%m-%dT00:00+02')
                        except Exception as e:
                                self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source format is not as expected',e)
                                return False

                        try:
                                df.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False, header=False)#headers=false
                        except Exception as e:
                                self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'cannot store data in file',e)
                                return False

                        print ("done")
                        return True
                else:
                        print('no files downloaded')
                        self.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source not found or cannot be open')
                        return False


        def producer(self,topic,msg,e=None):
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
                                if(a.copy_files_in_one()):
                                        a.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_INGESTION",'IMET VEHICLE SPEED data batch ingested to HDFS')
                        #end the Selenium browser session
                        d.close()
                        d.quit()

        except Exception as e:
                a.producer("THESS_ENV_IMET_SPEED_15MIN_DATA_ERROR",'data source not found or cannot be open',e)

