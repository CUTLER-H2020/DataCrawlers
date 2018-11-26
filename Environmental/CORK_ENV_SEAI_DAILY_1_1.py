# -*- coding utf-8 -*-
"""Provides facility to crawl and download csv files from target web platform and performs basic preprocessing for ISO time format"""
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import time
import os
import shutil
import uuid
import glob
import os
from time import gmtime, strftime
import pandas as pd
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

class oceanTides():

    def __init__(self):
        global downloadDir
        downloadDir = ""
        #Set Firefox preferences for headless crawling
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", downloadDir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk","attachment/csv")
        options = Options()
        options.add_argument("--headless")
        #Initialize webdriver and target URL
        self.driver = webdriver.Firefox(firefox_profile=fp,firefox_options=options)
        self.driver.implicitly_wait(15)
        self.driver.get("http://www.oceanenergyireland.com/testfacility/corkharbour/observations")
        self.verificationErrors = []
        self.accept_next_alert = True

    def crawl(self):
        driver = self.driver
        driver.execute_script("window.scrollTo(0, 600)")
        #Finds elements available on the target page
        index = 0
        driver.switch_to.frame(index)
        driver.find_element_by_xpath("//div[@id='CorkTideHeight']/div[3]/button[2]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//div[@id='CorkTideHeight']/div[3]/div/ul/li[5]").click()
        time.sleep(5)
        #Find the last downloaded file in target directory
        list_of_files = glob.glob('C:\\Users\\user\\PycharmProjects\\digitalOcean\\venv\\testdata1\\*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        df = pd.read_csv(latest_file, delimiter=';')
        #Format time into ISO 8601
        df['DateTime'] = pd.to_datetime(df['DateTime'], format='%Y-%m-%d%H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+00')
        #Adds current time at Cork for reading predictions
        timerecorded = strftime("%Y-%m-%dT%H:%M+00", gmtime())
        value = timerecorded
        valueArr = []
        for a in range( len(df) ):
            valueArr.append(value)
        raw_data = { 'PredictionDate': valueArr}
        df1 = pd.DataFrame(raw_data)
        upDF = pd.concat([df, df1], axis=1)
        upDF.to_csv(latest_file, index=False)
        #Move the changed file to target folder
        path = '' # Path for temp directory to be specified
        uFileName = str(uuid.uuid4())
        fileName = path + uFileName + ".csv"
        #Rename and move the file
        shutil.move("", fileName)
        driver.close()
        driver.quit()
        #os.system('pkill firefox')
        #os.system('pkill plugin-container')
        #os.system('pkill geckodriver')
if __name__ == '__main__':
    obj = oceanTides()
    obj.crawl()
