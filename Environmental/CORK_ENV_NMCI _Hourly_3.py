# -*- coding utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Hassan Mehmood, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Cork Harbour Weather. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" -This Crawler+Scraper requests the URL (Cork Harbour Weather) and fetches the HTML source of the target page"""
""" -The recieved page source is then parsed for available data"""
""" -The data is nested in nature which is splitted to form headers for relevant values and other special characters and UNITs are removed from data"""
""" -After cleaning data, it is stored in .CSV format with unique name"""
import requests
from bs4 import BeautifulSoup
import uuid
import csv
import dateutil.parser as parser
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

class corkHrb():
    """ This class initializes the crawling process by sending request to target URL and fetches the required information which is further stored in .CSV file"""
    def __init__(self):
        """Init function returns response from target URL"""
        #Definition of global variables to be used outside _init_ function
        global homePage
        global downloadDir
        global filname
        downloadDir = "" #Adds directory path for storing .CSV files
        uFileName = str(uuid.uuid4()) # Calls uuid library for unique file naming
        filname = downloadDir + uFileName + ".csv"
        homePage = requests.get("http://86.43.106.118/winfiles/cumulus/") # Sends request to target URL

    def pageHtml(self):
        """This function returns the formatted information from target HTML page and stores it as .CSV file in specified directory"""
        soup = BeautifulSoup(homePage.content, 'html.parser') #Initialize BS4 class to recieve page source
        new_data = [[[c.text for c in b.find_all('td')] for b in i.find_all('tr')] for i in soup.find_all('table')] #Finds all the tables including rows and columns
        _, *result = new_data
        *new_results, footer = [list(filter(None, i)) for b in result for i in b] #Filter values to form headers and respective values for each header
        grouped = [{c[i]: c[i + 1] for i in range(0, len(c), 2)} for c in new_results if len(c) > 1]
        filterList = [":"]
        headers = [i for b in grouped for i in b] #Collects headers from grouped items
        """The loop filters colon : values from headers and appends time column to track weather forecast"""
        for idz, var in enumerate(headers):
            for temp in filterList:
                headers[idz] = headers[idz].replace(temp, '')
        headers.append("Time")
        print(headers) #Prints formatted headers
        time1 = soup.find("caption") #Searches for time values added as caption in HTML table
        time2 = time1.get_text().split()
        filtter = ["Conditions", "at", "local", "time", "on"]
        filterList2 = [m for m in time2 if m not in filtter]
        filterList2 = ('\n'.join(filterList2))
        date = parser.parse(filterList2)
        timerecorded = (date.isoformat()) +"+00" #Formats time in ISO 8601 with timezone
        print(timerecorded)
        filterList2 = ['°C', 'W/m²', 'mm', 'mm/hr', 'mb', 'kts', 'mb/hr', '%','/hr', '°']
        values = [c[i] for i in headers for c in grouped if i in c]
        """The following loop filters UNITs defined with values and appends those values to []"""
        for idx, v in enumerate(values):
            for t in filterList2:
                values[idx] = values[idx].replace(t, '')
        values.append(timerecorded)
        print(values)
        """Writes extracted data to file as .CSV"""
        with open(filname, 'w', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar=',', lineterminator='\n')
            writer.writerow(headers)
            writer.writerow(values)
if __name__ == '__main__':
    objCall = corkHrb()
    objCall.pageHtml()
