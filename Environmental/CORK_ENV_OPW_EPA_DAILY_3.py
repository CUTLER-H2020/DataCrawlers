# -*- coding utf-8 -*-
""" -This Crawler+Scraper requests the URL (EPA (Environmental protection agency - Ground Water Level)) and fetches the HTML source of the target page"""
""" -The recieved page source is then parsed for available data"""
""" -The time is reported in UTC which is then converted to ISO 8601 format with UTC offset"""
""" -The data is cleaned for duplicate sensor readings"""
""" - After cleaning data, it is stored in .CSV format with unique name"""
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
from bs4 import BeautifulSoup
import uuid
import csv
import pandas as pd
import re
from datetime import datetime as dt
import glob
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"
class crawlHydro():

    def __init__(self):
        global downloadDir
        global uFileName
        global filname
        global tfilename
        downloadDir = ""
        newPath = ""
        uFileName = str(uuid.uuid4())
        filname = downloadDir + uFileName + ".csv"
        tfilename = newPath + uFileName + ".csv"
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        # Set Firefox preferences for headless crawling
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", downloadDir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                          "attachment/csv")
        options = Options()
        options.add_argument("--headless")
        # Initialize webdriver and target URL
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(15)
        self.driver.get("http://www.epa.ie/hydronet/#Groundwater")
        self.verificationErrors = []
        self.accept_next_alert = True

    def crawl(self):
        """This function fetches the data from the source and after cleaning stores it to .CSV file"""
        """The separated lines in function below needs to be commented for first execution and uncommented afterwards"""
        """---------------------------------------------------------------------------------------------------------------------"""
        list_of_files1 = glob.glob(
            '')  # Path to be added with * , * means all if need specific format then *.csv
        latest_file1 = max(list_of_files1, key=os.path.getctime)
        df_old = pd.read_csv(latest_file1, engine='python', sep=",")
        """---------------------------------------------------------------------------------------------------------------------"""
        driver = self.driver
        # Finds elements available on the target page for interaction/action
        driver.execute_script("window.scrollTo(0, 800)")
        driver.find_element_by_xpath('//td[.="Table"]').click()
        soup = BeautifulSoup(driver.page_source, 'html.parser') #Extract page content using BS4
        headers = []
        for m in soup.find_all("th"):
            headers.append(m.get_text())
        new_data = [[c.text.rstrip(" km²") for c in i.find_all('td')]  for i in soup.find_all('table')[5::]] #Extract table content i.e. column and rows
        new_data = [[dt.strptime(i, '%d-%m-%Y %H:%M').strftime('%d-%m-%YT%H:%M+00') if re.match("\d{2}-\d{2}-\d{4}\s\d{2}:\d{2}",i) else i for i in m] for m in new_data] # Convert time to ISO 8601
        finalDataList = []
        """Loop removes unnecessary rows"""
        for row in range(len(new_data) - 4):
            finalDataList.append(new_data[row])
        with open(filname, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(finalDataList)
        """Previously created file is compared with current readings to remove duplication"""
        """---------------------------------------------------------------------------------------------------------------------"""
        list_of_files = glob.glob(
            '')  # Path to be added with * , * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        df = pd.read_csv(latest_file, engine='python', sep=",")
        df1 = pd.merge(df, df_old, how='outer', indicator=True) #Merges old sensor data with new readings for filtering duplicates
        rows_in_df1_not_in_df2 = df1[df1['_merge'] == 'left_only'][df.columns]
        rows_in_df1_not_in_df2.to_csv(tfilename, index=False) # Make header false after first execution
        """---------------------------------------------------------------------------------------------------------------------"""
        # os.system('pkill firefox')
        # os.system('pkill plugin-container')
        # os.system('pkill geckodriver')clear

if __name__ == '__main__':
    obj = crawlHydro()
    obj.crawl()