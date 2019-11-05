# -*- coding utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Hassan Mehmood, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from WaterLevel OPW (http://waterlevel.ie). By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" -This Crawler+Scraper requests the URL (WaterLevel OPW) and fetches the JSON response of the target URL"""
""" -The recieved JSON response is then normalized using pandas"""
""" -The reported time is converted to ISO 8601"""
""" -The location data is separated to different columns (longitude and latitude)"""
""" - After formatting data, it is stored in .CSV format with unique name"""
import uuid
import pandas as pd
from time import gmtime, strftime, localtime
from datetime import datetime,timedelta
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import  pandas as pd
import uuid
class waterLevel():

   def __init__(self):
       global data
       global path
       global fileName
       pd.set_option('display.max_rows', 500)
       pd.set_option('display.max_columns', 500)
       pd.set_option('display.width', 1000)
       uFileName = str(uuid.uuid4())
       filname = path + uFileName + ".csv"
       request = ("http://waterlevel.ie/geojson/latest/")
       # request1.raise_for_status()
       response = urlopen(request)
       elevations = response.read()
       data = json.loads(elevations) #Loads the json file for normalization and parsing
       path = "" # Storage path to be added if required
   def fetchJson(self):
       dataList1 = []
       for values in data['features']:  # Loops through JSON data column and stores into list
           dataList1.append(values)
       jsonData = json_normalize(dataList1)  # Normalize nested data
       df2 = pd.DataFrame(jsonData.pop('geometry.coordinates').tolist()).astype(float)
       jsonData[['longitude', 'latitude']] = df2  # convert coordinates to longitude and latitude as separate
       jsonData['properties.datetime'] = pd.to_datetime(jsonData['properties.datetime'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+00')# Format time
       jsonData.to_csv(fileName, index=False)
if __name__ == '__main__':
   obj = waterLevel()
   obj.fetchJson()
