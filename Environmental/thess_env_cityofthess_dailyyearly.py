# -*- coding: utf-8 -*-

""" Download excel files and transform to correct format in csv files. """

""" Excel files are linked in href attribute of <a> elements in the given URL (Not nested URLs)"""
""" Each station, in stations array, is linked to a numerical code in this file"""
""" Longitude and latitude and location (as descriptive name) are added to each row of each station"""
""" Greek names for date and weekday are translated"""

# Code: thess_env_cityofthess_dailyyearly
# Code with numbering: thess_env_cityofthess_dailyyearly_1, thess_env_cityofthess_dailyyearly_2, thess_env_cityofthess_dailyyearly_3, thess_env_cityofthess_dailyyearly_4, thess_env_cityofthess_dailyyearly_5, thess_env_cityofthess_dailyyearly_6

# Stations (latitude, longitude):
# Egnatia (Στ. ΕΓΝΑΤΙΑΣ): Egnatia and I. Dragoumi (1st Municipal District) (40.63753, 22.94095): thess_env_cityofthess_dailyyearly_1
# Martiou (Στ. 25ης ΜΑΡΤΙΟΥ): 25 March and Karakasi (5th Municipal District) (40.60102, 22.96017): thess_env_cityofthess_dailyyearly_2
# Lagada (Στ. ΛΑΓΚΑΔΑ): Lagada and Koutifari (2nd Municipal District) (40.65233, 22.93514): thess_env_cityofthess_dailyyearly_3
# Eptapyrgio (Στ. ΕΠΤΑΠΥΡΓΙΟΥ): Agia Anastasia and Agrafon (3rd Diamersima) (40.64407, 22.95837): thess_env_cityofthess_dailyyearly_4
# Malakopi (Toumba) (Στ. ΜΑΛΑΚΟΠΗΣ): Harisio Girokomio (Dimitrios Charisis) (4th Diamersima) (40.61637, 22.98233): thess_env_cityofthess_dailyyearly_5
# Dimarxeio (Μτ.Στ. ΔΩΜΑ ΠΑΛ. ΔΗΜΑΡ.): King's George A (1st Diamersima) (40.62381, 22.95312): thess_env_cityofthess_dailyyearly_6

# NO, NO2, O3, PM10, PM2.5, CO, SO2
# μg/m3,μg/m3,μg/m3,μg/m3,μg/m3,mg/m3,μg/m3

from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import time
import os
from collections import deque
import pandas as pd
import shutil
import uuid
from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

log_file_path = '../../logger.log'

logging.basicConfig(filename=log_file_path, filemode='a', level=logging.INFO,
                    format='[%(asctime)s]%(name)s %(process)s {%(pathname)s:%(lineno)d}  %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S', )

code = 'thess_env_cityofthess_dailyyearly'
stations = {'Στ. ΕΓΝΑΤΙΑΣ': [40.63753, 22.94095], 'Στ. 25ης ΜΑΡΤΙΟΥ': [40.60102, 22.96017],
            'Στ. ΛΑΓΚΑΔΑ': [40.65233, 22.93514], 'Στ. ΕΠΤΑΠΥΡΓΙΟΥ': [40.64407, 22.95837],
            'Στ. ΜΑΛΑΚΟΠΗΣ': [40.61637, 22.98233], 'Μτ.Στ. ΔΩΜΑ ΠΑΛ. ΔΗΜΑΡ.': [40.62381, 22.95312]}
names = {'Στ. ΕΓΝΑΤΙΑΣ': 'Egnatia', 'Στ. 25ης ΜΑΡΤΙΟΥ': 'Martiou', 'Στ. ΛΑΓΚΑΔΑ': 'Lagada',
         'Στ. ΕΠΤΑΠΥΡΓΙΟΥ': 'Eptapyrgio', 'Στ. ΜΑΛΑΚΟΠΗΣ': 'Malakopi', 'Μτ.Στ. ΔΩΜΑ ΠΑΛ. ΔΗΜΑΡ.': 'Dimarxeio'}
origin_url = 'https://opendata.thessaloniki.gr/el/dataset/%CE%BC%CE%B5%CF%84%CF%81%CE%AE%CF%83%CE%B5%CE%B9%CF%82-%CE%B4%CE%B7%CE%BC%CE%BF%CF%84%CE%B9%CE%BA%CE%BF%CF%8D-%CE%B4%CE%B9%CE%BA%CF%84%CF%8D%CE%BF%CF%85-%CF%83%CF%84%CE%B1%CE%B8%CE%BC%CF%8E%CE%BD-%CE%B5%CE%BB%CE%AD%CE%B3%CF%87%CE%BF%CF%85-%CE%B1%CF%84%CE%BC%CE%BF%CF%83%CF%86%CE%B1%CE%B9%CF%81%CE%B9%CE%BA%CE%AE%CF%82-%CF%81%CF%8D%CF%80%CE%B1%CE%BD%CF%83%CE%B7%CF%82-%CF%84%CE%BF%CF%85-%CE%B4%CE%AE%CE%BC%CE%BF%CF%85-%CE%B8%CE%B5%CF%83%CF%83%CE%B1%CE%BB%CE%BF%CE%BD%CE%AF%CE%BA%CE%B7%CF%82'

l_temp_path = '/home/oulu/THESS/data/environmental/temp/thess_env_cityofthess_dailyyearly/'
l_final_path = '/home/oulu/THESS/data/environmental/thess_env_cityofthess_dailyyearly/'

WINDOW_SIZE = "1920,1080"


class thess_env_cityofthess_dailyyearly(object):

    def __init__(self, url):
        self.url = url
        self.xlfnames = []
        self.url_queue = deque([])  # doble-ended queu
        self.folder = l_temp_path

    def get_page(self, url):
        """ Downloiad the page at given URL"""
        """ @param url: Url we want to crawl"""
        """ @type url: String """
        """@return the page"""
        try:
            u = urlopen(url)
            html = u.read().decode('utf-8')
        # except Exception as e:
        # logging.exception(e)
        finally:
            print("Closing")
            u.close()
            return html

    def get_soup(self, html):
        """Returns the BeautifulSoup object of the given page"""
        if html is not None:
            soup = BeautifulSoup(html, "html.parser")
            return soup
        else:
            return

    def get_links(self, soup):
        """Get the links of interest from the given Beuti"""
        """ @param soup: BeautifulSoup object that cointains the targeted links """
        """ @type soup: BeautifulSoup object """
        for link in soup.select('a[href^="https://"]'):  # All links which have a href element
            href = link.get('href')  # The actually href element of the link
            if not any(href.endswith(x) for x in ['.csv', '.xls', '.xlsx']):
                print("No excel")
                continue
            if not href in self.url_queue:
                self.url_queue.append(href)  # Add the URL to our queue

    def get_files(self):
        """Create a temp folder to download"""
        # self.folder= +str(int(time.time()))
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        while len(self.url_queue):  # If we have URLs to crawl - we crawl
            href = self.url_queue.popleft()  # We grab a URL from the left of the list
            filename = href.rsplit('/', 1)[-1]
            print("Downloading %s to %s..." % (href, filename))
            fullname = os.path.join(self.folder, filename)
            urlretrieve(href, fullname)
            self.xlfnames.append(filename)

    def run_downloader(self):
        """downloads the htmlpage and looks for the links with excel files"""
        """calls to the file downloader"""
        try:
            html = self.get_page(self.url)
            soup = self.get_soup(html)
            if soup is not None:  # If we have soup -
                self.get_links(soup)
                self.get_files()
            else:
                self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR", 'data source format is not as expected',
                              e)
                return False
        except Exception as e:
            self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR", 'data source format is not as expected', e)

            return False
        return True

    def parse_sheet_to_df(self, xl, sheet, df):
        """ @param xl: excel file object  """
        """ @type xl: dataframe """
        """ @param sheet: sheet object  """
        """ @type sheet: dataframe """
        if sheet in stations.keys():
            # Create dataframe. Note, put this out of the loop to write all the sheets in same csv file
            # df = pd.DataFrame()
            # print(sheet.encode('utf-8'))

            df_tmp = xl.parse(sheet)

            # Clean the data
            # replace return, remove units
            df_tmp.columns = df_tmp.columns.str.replace('\n', ' ').str.strip(' μg/m3').str.strip(' mg/m3')
            # select the columns of interest
            df_tmp = df_tmp.filter(regex='(NO|NO2|O3|PM10|PM2,5|CO|SO2|Ημερο - μηνία|Ημέρα)')
            # df_tmp.columns = df_tmp.columns.str.strip(' μg/m3').str.strip(' mg/m3')
            # correct format of information
            df_tmp['Ημέρα'] = df_tmp['Ημέρα'].dt.day_name()
            df_tmp['Latitude'] = stations[sheet][0]
            df_tmp['Longitude'] = stations[sheet][1]
            df_tmp['Location'] = names[sheet]

            # renaming fields in greek
            df_tmp.rename(columns={'Ημερο - μηνία': 'Date', 'Ημέρα': 'Weekday'}, inplace=True)

            df_tmp.rename(columns={'NO': 'air_pollution_NO', 'NO2': 'air_pollution_NO2', 'O3': 'air_pollution_O3',
                                   'PM10': 'air_pollution_PM10', 'PM2,5': 'air_pollution_PM25',
                                   'CO': 'air_pollution_CO', 'SO2': 'air_pollution_SO2'}, inplace=True)

            return df_tmp

    def write_to_file(self, df):
        try:
            # Directory name bydata/ code/codenumber
            if not os.path.exists(l_final_path):
                os.mkdir(l_final_path)
            outerdir = l_final_path + code
            if not os.path.exists(outerdir):
                os.mkdir(outerdir)
            # CODE FOR JUST ONE FOLDER
            outdir = outerdir

            # CODE FOR MANY FOLDER
            # outdir = outerdir+'/'+code+'_'+str(list(stations).index(sheet)+1)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
        except Exception as e:
            self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR", 'cannot create folder/file to store data', e)
            return False
        try:
            # Write to the csv file.
            # Note, put this out of the loop to write all the sheets in same csv file
            csvfile = str(uuid.uuid4()) + ".csv"  # sheet+'.csv'
            fullname = os.path.join(outdir, csvfile)
            df.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False)  # mode a is append
        except Exception as e:
            # logging.exception('exception happened')
            self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR", 'cannot store data in file')
            return False
        return True

    def parse_files(self):
        """ calls parse_sheet to each sheet in the given file """
        """ @param name: name of the file  """
        """ @type name: string """
        df = pd.DataFrame()
        if not self.xlfnames:
            self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR", 'data source not found or cannot be open')
            logging.error('error happened: no excel files found')
            return False
        for fileName in self.xlfnames:
            try:
                xlfname = self.folder + '/' + fileName  #
                xl = pd.ExcelFile(xlfname)
            except Exception as e:
                self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR",
                              'data source not found or cannot be open', e)
                return False
            try:
                # code for one file per sheet
                # for sheet in xl.sheet_names:
                #       self.parse_sheet(xl,sheet)

                # code for one file for all
                for sheet in xl.sheet_names:
                    df_tmp = self.parse_sheet_to_df(xl, sheet, df)
                    df = df.append(df_tmp, ignore_index=True)
            except Exception as e:
                self.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_ERROR", 'data source format is not as expected',
                              e)
                return False
        return self.write_to_file(df)

    def producer(self, topic, msg, e=None):
        """ This function sends data to kafka bus"""
        producer = KafkaProducer(bootstrap_servers=['HOST_IP', 'HOST_IP', 'HOST_IP']
                          ,api_version=(2, 2, 1),security_protocol='SSL',
                          ssl_check_hostname=True,
                          ssl_cafile='/home/oulu/certs/ca-cert',
                          ssl_certfile='/home/oulu/certs/cutler-p3-c1-00.crt',
                          ssl_keyfile='/home/oulu/certs/cutler-p3-c1-00.key')

        msg_b = str.encode(msg)
        producer.send(topic, msg_b).get(timeout=30)

        if (e):
            logging.exception('exception happened')


if __name__ == '__main__':
    a = thess_env_cityofthess_dailyyearly(origin_url)
    if (a.run_downloader()):
        if (a.parse_files()):
            a.producer("THESS_ENV_CITYOFTHESS_DAILY_YEARLY_DATA_INGESTION",
                       'City of Thessaloniki environmental data ingested to HDFS')
