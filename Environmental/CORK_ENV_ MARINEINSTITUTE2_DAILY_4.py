# -*- coding utf-8 -*-
""" -This Crawler+Scraper requests the URL (Marine institute Tide Predictions) and fetches the HTML source of the target page"""
""" -The recieved page source is then parsed for available data"""
""" -The time is reported in UTC with Z-Zulu extension which is then converted to UTC offset"""
""" -The data is cleaned for removing reported units from Html Table"""
""" - After cleaning data, it is stored in .CSV format with unique name"""
import uuid
import pandas as pd
from time import gmtime, strftime, localtime
from datetime import datetime,timedelta
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

class tidePredictionsMarine():
    """ This class initializes the crawling by sending request to target URL and fetches the required information which is further stored in .CSV file"""
    def __init__(self):
        global homePage
        global downloadDir
        global fileName
        global finalUrl
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        downloadDir = ""#Adds directory path for storing .CSV files
        uFileName = str(uuid.uuid4())# Calls uuid library for unique file naming
        fileName = downloadDir + uFileName + ".csv"
        homePage = "https://erddap.marine.ie/erddap/tabledap/IMI-TidePrediction.htmlTable?time,longitude,latitude,stationID,Water_Level&time%3E="
        time1 = datetime.now() + timedelta(days=3)
        time2 = str(time1.strftime("%Y-%m-%dT"))
        time2 = time2 + "00:00:00Z"
        showtime = str(strftime("%Y-%m-%dT", localtime()))
        showtime = showtime + "00:00:00Z"
        finalUrl = (homePage + showtime + "&time%3C=" + time2 + "&stationID=%22Crosshaven_MODELLED%22")
        print(finalUrl)
    def readHtml(self):
        """This function reads the response  from request made to REST like URL query
                   and returns the response which is further  formatted and stored as .CSV file
                    in specified directory"""
        iDf = pd.read_html(finalUrl)#Reads the html table
        df = iDf[1]
        df = df.drop(1, axis=0)
        df = df.reset_index(level=0, drop=True, inplace=False)
        upDF = df.replace({'Z': '+00'}, regex=True)
        # print(upDF)
        timerecorded = strftime("%Y-%m-%dT%H:%M+00", gmtime())
        value = timerecorded
        valueArr = ['PredictionDate']
        """This loop adds PredictionDate column to track values from dataset model,
                 the column will contain current local time of cork specifying that last 
                 prediction was fetched from datset at this time"""
        for a in range(len(upDF) - 1):
            valueArr.append(value)
        raw_data = {'6': valueArr}
        df1 = pd.DataFrame(raw_data)
        upDF = pd.concat([upDF, df1], axis=1)
        #upDF = upDF.drop(0, axis=0)#uncomment after first execution, removes header
        upDF.to_csv(fileName, index=False, header=None)#Store Fetched data to specified directory as .CSV

if __name__ == '__main__':
    objCall = tidePredictionsMarine()
    objCall.readHtml()
