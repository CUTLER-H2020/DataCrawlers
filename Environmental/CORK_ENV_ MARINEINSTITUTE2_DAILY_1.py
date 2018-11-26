# -*- coding utf-8 -*-
""" -This Crawler+Scraper requests the URL (Marine institute Wave Forecast observations) and fetches the HTML source of the target page"""
""" -The recieved page source is then parsed for available data"""
""" -The time is reported in UTC with Z-Zulu extension which is then converted to UTC offset"""
""" -The data is cleaned for removing reported units from Html Table"""
""" - After cleaning data, it is stored in .CSV format with unique name"""
import uuid
import pandas as pd
from time import gmtime, strftime, localtime
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

class waveForecastMarine():
    """ This class initializes the crawling by sending request to target URL and fetches the required information which is further stored in .CSV file"""
    def __init__(self):
        """Init function  creates REST like URL query for requesting HTML page containing dataset"""
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
        """URL query is created by using all field information given on this document https://erddap.marine.ie/erddap/rest.html """
        homePage = "https://erddap.marine.ie/erddap/griddap/IMI_EATL_WAVE.htmlTable?"
        showtime = str(strftime("%Y-%m-%dT", localtime()))
        showtime = showtime + "00:00:00Z"
        coordinate= "[(51.1965):1:(51.8939)][(-9.3524):1:(-7.6532)]"
        duration = "[(" +showtime+"):1:("+showtime+")]"+ coordinate
        finalUrl = (homePage + "significant_wave_height"+duration+",swell_wave_height"+duration+",mean_wave_direction"+duration+",mean_wave_period"+duration)

    def readHtml(self):
        """This function reads the response a from request made to REST like URL query
                  and returns the response which is further  formatted and stored as .CSV file
                   in specified directory"""
        iDf = pd.read_html(finalUrl) #Reads the html table
        df = iDf[1]
        df = df.drop(1, axis=0)
        df = df.reset_index(level=0, drop=True, inplace=False)
        upDF = df.replace({'Z': '+00'}, regex=True)
        #upDF = df.drop(0,axis=0) # To be uncommented after first execution (Removes headers)
        upDF.to_csv(fileName, index=False, header=None) #Store Fetched data to specified directory as .CSV
if __name__ == '__main__':
    objCall = waveForecastMarine()
    objCall.readHtml()

