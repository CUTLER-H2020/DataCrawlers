# -*- coding: utf-8 -*-

"""Download data from html tables into csv, with scheduled update (daily)"""

""" Data is in html tables that are displayed when choosing the adequate values in <select> elements"""
""" <select id = fyear> Just current option (which is current year)"""
""" <select id = esex> with option values = 1,0 with text values = Έσοδα,Έξοδα  (Income,Expenses)"""
""" All the data (Income and Expenses) are stored in the same output file."""
""" Type, that is Income or Expenses, is added as a column"""
""" Year is added as a column"""
""" Greek names are translated"""
""" Note: Directorate value is Δεν υπάρχουν αποτελέσματα when no results (sometimes retrieving one year fails)"""
""" Note: if Local is set to False, the browser runs in headless mode"""

""" Note: there should be a file with the batch data at temp, were new data woul be stored. This file is checked in order to know is there is actually new data  """

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import pandas as pd
import os
import shutil
import uuid
# import sys


from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

#log_file_path = '../../logger.log'

logging.basicConfig(level=logging.INFO)

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

origin_url = 'https://gaiacrmkea.c-gaia.gr/city_thessaloniki/index.php'
code = 'thess_eco_thessaloniki_municipality_budget'
path_to_webdriver_c = '/usr/bin/chromedriver'
#path_to_webdriver_f = 'C:\\Users\\martacor\\Development\\python\\cuttler\\libs\\geckodriver.exe'
# path_to_webdriver = 'C:\\Users\\Owner\\Documents\\development\\cutler\\code\\libs\\chromedriver.exe'
options = {'Έξοδα': 'Expenses', 'Έσοδα': 'Income'}  # Exoenses, Income
# local
l_temp_path = '/home/oulu/THESS/data/economic/temp/'
l_final_path = '/home/oulu/THESS/data/economic/thess_eco_thessaloniki_municipality_budget/'
l_store_file = 'thessaloniki_budget.csv'
l_store_path = l_temp_path

WINDOW_SIZE = "1920,1080"
temp_path = ''
final_path = '/home/oulu/THESS/data/economic/thess_eco_thessaloniki_municipality_budget/'  # +code


class thess_eco_thessaloniki_municipality_budget(object):

    def __init__(self, url):
        self.url = url
        self.local = True
        self.file_to_move = ''
    def get_session(self):
        """Initialize webdriver and target URL, depending on environment"""

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        # chrome_options.put("download.default_directory",downloadFilepath);
        # mainPath = os.getcwd()
        #downloadFilepath = os.path.normpath(mainPath + downloadFileFolder)
        #preferences = {"download.default_directory": downloadFilepath, "directory_upgrade": True, "safebrowsing.enabled": True}
        #chrome_options.add_experimental_option("prefs", preferences)
        self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=chrome_options)  # ,chrome_options=chrome_options)
        self.driver.get(self.url)
        self.driver.implicitly_wait(60)
        # self.driver.maximize_window()
        # self.driver.implicitly_wait(30)
        self.driver.get(self.url)  # self.verificationErrors = []
        #
        return self.driver


    # except:
    #   print(sys.exc_info()[0],"occured.")
    #   return False

    def parse_tables(self, driver):

        try:
            # first, get file with old values
            outerdir = l_temp_path
            if not os.path.exists(outerdir):
                os.mkdir(outerdir)
            outdir = outerdir + code
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            csvfile = l_store_file

            # file to save/reaad from for comparation
            filename = os.path.join(outdir, csvfile)
            # temporary file for merging and cleaning
            filename2 = os.path.join(outdir, 'thessaloniki_budget.csv')
            print('file name to open ' + filename)

            try:
                df_old = pd.read_csv(filename, engine='python', encoding='utf-8-sig', sep=",")
            except:
                df_old = pd.DataFrame()
                print('not file found')
            df_new = pd.DataFrame()
            select = Select(driver.find_element_by_id('esex'))
            typeoptions = [to.text for to in select.options]
            for option in typeoptions:
                # Directory name by code/codenumber
                select.select_by_visible_text(option)
                select = Select(driver.find_element_by_id('esex'))
                # print('primary select')

                select_y = Select(driver.find_element_by_id('fyear'))
                selected_option = select_y.first_selected_option
                year = selected_option.text
                # print(year)

                # print('get soup level 2')
                soup_level2 = BeautifulSoup(driver.page_source, 'lxml')
                # Beautiful Soup grabs the HTML table on the page
                # print('get tables')
                tables = soup_level2.find_all('table')
                # print('get just one table')
                table = tables[1]
                # Giving the HTML table to pandas to put in a dataframe object
                # read_html() produces a list of dataframes
                # print ('create dataframe list')
                df = pd.read_html(str(table), header=0)
                # print ('add year')
                # Add new columns
                df[0]['Year'] = year
                df[0]['Type'] = options[option]
                # renaming fields in greek
                df[0].rename(columns={'Υπηρεσία': 'DIRECTORATE', 'Κ.Α.': 'CODE_NUMBER', 'Περιγραφή': 'DESCRIPTION',
                                      'Προϋπολογισθέντα': 'PROJECTED_REVENUES', 'Διαμορφωθέντα': 'ACTUAL_REVENUES',
                                      'Δεσμευθέντα': 'COMMITMENTS', 'Ενταλθέντα': 'PAYMENTS_ORDERS',
                                      'Πληρωθέντα': 'PAID_LIABILITIES', 'Βεβαιωθέντα': 'ESTABLISHED_REVENUES',
                                      'Εισπραχθέντα': 'COLLECTED_REVENUES'}, inplace=True)
                dft = df[0]
                # print(dft.dtypes)
                # Note: Directorate value is Δεν υπάρχουν αποτελέσματα when no results
                # cleaning the 'no values' rows
                dft['DIRECTORATE'] = dft['DIRECTORATE'].astype(str)
                dft = dft[dft['DIRECTORATE'] != 'Δεν υπάρχουν αποτελέσματα']
                # print ('appending to df_old')
                df_new = df_new.append(dft, ignore_index=True)
                # print ('******new')
                # print(df_new.dtypes)

                # refresh select object
                select = Select(driver.find_element_by_id('esex'))

            df_new.to_csv(filename2, mode='w', encoding='utf-8-sig', index=False)
            df_new2 = pd.read_csv(filename2, engine='python', encoding='utf-8-sig', sep=",")
            # print ('******old')
            # print (df_old.dtypes)
            # print ('******new 2')
            # print (df_new2.dtypes)
            # get just new values_ those that are in df_new2 that are not in df_old
            df_temp = pd.merge(df_new2, df_old, how='outer', indicator=True)
            rows_in_df_not_in_dfold = df_temp[df_temp['_merge'] == 'left_only'][df_new2.columns]
        except Exception as e:
            self.producer("THESS_ECO_THESSALONIKI_MUNICIPALITY_BUDGET_DATA_ERROR",
                          'data source format is not as expected', e)
            return False
        # Create file to save new data
        # Move the changed file to target folder
        # Update stored info with new info for comparison
        if not rows_in_df_not_in_dfold.empty:
            try:
                # print ('New rows')

                # copy to corresponding files
                # create folder structure for temporary file that will be moved to code folder
                touterdir = l_temp_path
                if not os.path.exists(touterdir):
                    os.mkdir(touterdir)
                toutdir = touterdir + code
                if not os.path.exists(toutdir):
                    os.mkdir(toutdir)
                csvfile = str(uuid.uuid4()) + ".csv"
                tfilename = os.path.join(outdir, csvfile)

            except Exception as e:
                self.producer("THESS_ECO_THESSALONIKI_MUNICIPALITY_BUDGET_DATA_ERROR",
                              'cannot create folder/file to store data', e)
                return False
            try:
                # build filename for only new values in code folder

                fpath = l_final_path + code + '/'
                file_new_values = fpath + csvfile
                # copy to file with only new values
                # store new values in temporary file in temp folder
                rows_in_df_not_in_dfold.to_csv(tfilename, mode='w', encoding='utf-8-sig', index=False)
                f_outerdir = l_final_path
                if not os.path.exists(f_outerdir):
                    os.mkdir(f_outerdir)
                f_outdir = f_outerdir + code
                if not os.path.exists(f_outdir):
                    os.mkdir(f_outdir)
                # move the file to the correct place in code folder
                shutil.move(l_store_path + code + '/' + csvfile, file_new_values)
                # finally add new values to old temporary in temp folder
                # print ('appending to df_old')
                df_old = df_old.append(rows_in_df_not_in_dfold, ignore_index=True)
                df_old.to_csv(filename, mode='w', encoding='utf-8-sig', index=False)  # header=False
            except Exception as e:
                self.producer("THESS_ECO_THESSALONIKI_MUNICIPALITY_BUDGET_DATA_ERROR", 'cannot store data in file', e)
                return False
        return True

    def producer(self, topic, msg, e=None):
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
    a = thess_eco_thessaloniki_municipality_budget(origin_url)
    try:
        d = a.get_session()
    except Exception as e:
        a.producer("THESS_ECO_THESSALONIKI_MUNICIPALITY_BUDGET_DATA_ERROR", 'data source not found or cannot be open', e)
    if (d):
        if (a.parse_tables(d)):
            a.producer("THESS_ECO_THESSALONIKI_MUNICIPALITY_BUDGET_DATA_INGESTION",
                       'Municipality budget for Thessaloniki data ingested to HDFS')
        d.close()
        d.quit()
