# -*- coding utf-8 -*-
""" -This Crawler+Scraper requests the URL (Irish Meteorological Service - Met Eireann ) and fetches the HTML source of the target page"""
""" -The recieved page source is then parsed for available data"""
""" -The time is reported as long string (LATEST WEATHER REPORTS ON 07-NOV-2018 FOR 14:00) which is then cleaned for unncessary words"""
""" -After cleaning the time is converted to ISO 8601"""
""" -Because of nested structure of HTML headers are re-arranged and renamed"""
import requests
from bs4 import BeautifulSoup
import uuid
import pandas as pd
import dateutil.parser as parser
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

class metEirean():
    """ This class initializes the crawling by sending request to target URL and fetches the required information which is further stored in .CSV file"""
    def __init__(self):
        global homePage
        global downloadDir
        global fileName
        global homePage
        global homePage1
        #pd.set_option('display.height', 1000)
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        downloadDir = ""#Adds directory path for storing .CSV files
        uFileName = str(uuid.uuid4())# Calls uuid library for unique file naming
        fileName = downloadDir + uFileName + ".csv"
        homePage = requests.get("https://www.met.ie/latest-reports/observations")#URL to be requested
        homePage1 = ("https://www.met.ie/latest-reports/observations")#URL to be requested

    def readHtml(self):
        """This function reads the response  from request made to URL
                          and returns the response which is further  formatted and stored as .CSV file
                           in specified directory"""
        iDf = pd.read_html(homePage1)# Reads the html table
        iDfN = iDf[0]
        iDfN.columns = iDfN.columns.droplevel(-1) #Remove sub-headers
        iDfN = iDfN.rename(columns={'Wind': 'Wind Direction', 'Weather': 'Wind Speed', 'Temp': 'Weather', 'Humidity': 'Temp', 'Rain': 'Humidity', 'Pressure': 'Rain', 'Unnamed: 7_level_0': 'Pressure'})#Rename headers
        soup = BeautifulSoup(homePage.content, 'html.parser')
        time = soup.find("h2")#get time from captions
        time = time.get_text().split()
        filterList = ["Latest", "Weather", "Reports", "on","FOR"]
        filterList1 = [m for m in time if m not in filterList] # Filter sentence based time
        strippedTime = ('\n'.join(filterList1))
        date = parser.parse(strippedTime)
        timerecorded = (date.isoformat()) # Format stripped time to ISO 8601
        value = timerecorded+"+00"
        valueArr = []
        for a in range( len(iDfN) ):
            valueArr.append(value)
        raw_data = { 'ForecastTime': valueArr}
        df = pd.DataFrame(raw_data)
        oDf = pd.concat([iDfN, df], axis=1)
        oDf.to_csv(fileName, index=False) # saved file to specified directory as .CSV & mark header false after first execution
if __name__ == '__main__':
    objCall = metEirean()
    objCall.readHtml()
