# -*- coding: utf-8 -*-

""" Parse excel files into correct format in csv files. """
""" """
""" Data is distributed in two excel files. Each excel file has the data for 6 of the stations, a sheet per station"""
""" There is a sheet also in each file named ALLES with cleaned data for the corresponding to the 6 stations: we parse this one """
""" ALLES sheet has two columns per station (one of them is hidden), with naming of the form Pn and Pn.1 (Pn: id of the station)"""
""" We are interested in the column with name Pn"""
""" Date time is the first column with the format YYY.MM.DD HH:mm:ss"""
""" There is a sheet in another excel file, with the names, id and location of each station"""
""" Location information is in X, Y coordinates (Belgian Lambert 72, EPSG:31370) http://http://spatialreference.org/ref/epsg/31370/"""
"""

"""
""" Original files must be previously saved in folder temp/code_name"""
""" """
""" code: ant_env_cityofant_histprec """
""" code with numbering:  ant_env_cityofant_histprec-P1, ant_env_cityofant_histprec-P2, ant_env_cityofant_histprec-P3, ant_env_cityofant_histprec-P4, ant_env_cityofant_histprec-P5, ant_env_cityofant_histprec-P6, """
"""                                     ant_env_cityofant_histprec-P7, ant_env_cityofant_histprec-P8, ant_env_cityofant_histprec-P9, ant_env_cityofant_histprec-P10, ant_env_cityofant_histprec-P11, ant_env_cityofant_histprec-P12     """

import os
import pandas as pd
import shutil
import uuid
#import pytz
import datetime

from kafka import KafkaProducer
from kafka.errors import KafkaError


__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

import logging

#log_file_path = '../../logger.log'


logging.basicConfig(level=logging.DEBUG)

code = "ant_env_cityofant_histprec"
xlfnames =['alladata_v20_deel1.xlsx','alladata_v20_deel2.xlsx']
xlflocations = 'sensors_antwerpen.xlsx'

l_temp_path = '/home/oulu/ANT/data//temp/'
l_final_path = '/home/oulu/ANT/data/environmental/'
names_sheetn = 'sensors'
clean_data_sheetn = 'ALLES'

class ant_env_cityofant_histprec (object):

        def _init_(self):
                self.local = True

        def parse_files(self):

                #first, parse sensor locations
                try:
                        #first, parse sensor locations
                        xlflocationsname = l_temp_path+code+'/'+xlflocations
                        xl_l = pd.ExcelFile(xlflocationsname)
                        df_stations = xl_l.parse(names_sheetn)

                except Exception as e:
                        #logging.exception('exception happened')
                        self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'data source not found or cannot be open',e)
                        return False
                #df_stations.rename(columns={df_stations.columns[3]:'Longitude',df_stations.columns[4]:'Latitude', 'NAAM':'Name'},inplace=True)

                ## Create data file structure
                try:

                        #Note, put this out of the loop to write all the sheets in same csv file
                        #create folder/file structure
                        outdir = l_final_path+code
                        if not os.path.exists(outdir):
                                os.mkdir(outdir)
                except Exception as e:
                        self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'cannot create folder/file to store data',e)
                        return False
                try:
                #Write to the csv file.
                        csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
                        #print ('create folder '+code+'_'+name)
                        fullname = os.path.join(outdir, csvfile)

                        #df.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False)
                except Exception as e:
                        print(e)
                        #logging.exception('exception happened')
                        self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'cannot store data in file',e)
                        return False


                try:


                        #second, parse data
                        for fileName in xlfnames:
                                try:
                                        xlfname = l_temp_path+code+'/'+fileName#
                                        xl = pd.ExcelFile(xlfname)
                                        print ('opening file '+fileName)
                                except Exception as e:
                                        self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'data source not found or cannot be open',e)
                                        return False

                                df_clean_data = xl.parse (clean_data_sheetn)
                                df_clean_data.reset_index(inplace = True)
                                df_clean_data.rename(columns={df_clean_data.columns[0]:'DateTime'},inplace=True)
                                df_temp = pd.DataFrame()
                                print('here1')
                                for column in df_clean_data:

                                        #Directory name by code/codenumber
                                        if column != 'DateTime' and column.find('.')!=-1:
                                                #print ('on column '+column)
                                                name =column.split(".")[0]
                                                #print ('on column name '+name)
                                                #new datagram with the station values
                                                #df_temp = df_clean_data [df_clean_data.columns[0], column]#.to_csv(fullname, mode='w', encoding='utf-8', index=False)
                                                df_temp = df_clean_data [['DateTime',column]].copy()
                                                #df_temp [name]= df_clean_data [column]
                                                df_temp.rename(columns={column:'Rainfall'},inplace=True)
                                                #Format time into ISO 8601
                                                df_temp['DateTime'] = pd.to_datetime(df_temp['DateTime'], format='%Y/%m/%d%H:%M:%S').dt.strftime('%Y-%m-%dT%H:%M+01')
                                                #get the values of the station
                                                yl = df_stations.loc[df_stations['NR'] == name,'Y'].item()
                                                xl = df_stations.loc[df_stations['NR'] == name,'X'].item()
                                                #print ('x is '+str(xl))
                                                #print ('y is '+str(yl))
                                                df_temp['Y'] = yl
                                                df_temp['X'] = xl
                                                #TODO Format X Y into Latitude Longitude if needed
                                                #df_temp['Latitude'] = df_stations.loc[df_stations['NR'] == name,'Y'].item()#  int(s),'Latitude']
                                                #df_temp['Longitude'] = df_stations.loc[df_stations['NR'] == name,'X'].item()#int(s),'Longitude']
                                                df_temp['Location'] = df_stations.loc[df_stations['NR'] == name,'LOCATIOn'].item()#int(s),'Name']
                                                df_temp['NR'] = df_stations.loc[df_stations['NR'] == name,'NR'].item()


                                                df_temp.rename(columns={'NR':'sensor_id'},inplace=True)

                                                ##########################################

                                                df_temp.to_csv(fullname, mode='a', encoding='utf-8-sig', index=False)

                                                #########################################



                except Exception as e:
                        #logging.exception('exception happened')
                        print (e)
                        self.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_ERROR",'data source format is not as expected',e)

                        return False

                return True


        def producer(self,topic,msg, e=None):
           producer = KafkaProducer(bootstrap_servers=['HOST_IP', 'HOST_IP', 'HOST_IP']
                          ,security_protocol='SSL',
                          ssl_check_hostname=True,
                          ssl_cafile='/home/oulu/certs/ca-cert',
                          ssl_certfile='/home/oulu/certs/cutler-p01-c2-0.crt',
                          ssl_keyfile='/home/oulu/certs/cutler-p01-c2-0.key')
           msg_b = str.encode(msg)
           producer.send(topic, msg_b).get(timeout=30)
           if (e):
             logging.exception('exception happened')
if __name__ == '__main__':
        a = ant_env_cityofant_histprec()
        if (a.parse_files()):
                a.producer("ANT_ENV_CITYOFANT_HISTPREC_DATA_INGESTION",'Historic precipitation data for antwerp ingested to HDFS')
