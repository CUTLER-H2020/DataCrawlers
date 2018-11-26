# -*- coding utf-8 -*-
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
