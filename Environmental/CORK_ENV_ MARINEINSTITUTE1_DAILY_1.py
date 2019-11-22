# -*- coding utf-8 -*-

""" This code is open-sourced software licensed under the MIT license (http://opensource.org/licenses/MIT)""" 
""" Copyright  2019 Hassan Mehmood, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Irish weather buoys network-Marine institute. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 
""" -This Crawler+Scraper requests the URL (Irish weather buoys network-Marine institute) and fetches the HTML source of the target page"""
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

class marineIns():
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
        time1 = datetime.now() - timedelta(days=1)
        time2 = str(time1.strftime("%Y-%m-%dT"))
        time2 = time2 +"00:00:00Z"
        showtime = str(strftime("%Y-%m-%dT", localtime()))
        showtime = showtime + "00:00:00Z"
        """URL query is created by using all field information given on this document https://erddap.marine.ie/erddap/rest.html """
        dailyUrl = "https://erddap.marine.ie/erddap/tabledap/IWBNetwork.htmlTable?time,longitude,latitude,AtmosphericPressure,WindDirection,WindSpeed,Gust,WaveHeight,WavePeriod,MeanWaveDirection,Hmax,AirTemperature,DewPoint,SeaTemperature,salinity,RelativeHumidity,QC_Flag,station_id&time%3E="
        finalUrl = (dailyUrl + time2 + "&time%3C=" + showtime)
    def readHtml(self):
        """This function reads the response  from request made to REST like URL query
                  and returns the response which is further  formatted and stored as .CSV file
                   in specified directory"""
        iDf = pd.read_html(finalUrl)#Reads HTML table on requested URL
        df = iDf[1]# specifying which table will be used for scraping data
        df = df.drop(1, axis=0)
        df = df.reset_index(level=0, drop=True, inplace=False)
        upDF = df.replace({'Z': '+00'}, regex=True)# Searches for ZULU as Z and formats the time to ISO 8601 by adding UTC offset
        #upDF = upDF.drop(0, axis=0)#uncomment after first execution, removes header
        upDF.to_csv(fileName, index=False, header=None)#Store Fetched data to specified directory as .CSV

if __name__ == '__main__':
    objCall = marineIns()
    objCall.readHtml()
