# -*- coding: utf-8 -*-

""" Parse excel file into correct format in csv files. """
""" """
"""	Data are stored in an excel file named gelir-gider.xlsx in a table"""
""" Columns names:
	-Visitor Ticket ->code: anta_eco_cityofantalya_visitorticket_monthly
	-Entrance Fee ->code: anta_eco_cityofantalya_visitorticket_monthly
	-Otopark Ticket	-> code: anta_eco_citiofantalya_otopark_monthly
	-Parking Fee ->code: anta_eco_citiofantalya_otopark_monthly
	-NO -> Shop Rent -> code: anta_eco_cityofantalya_ShopsRentEarn_year
	-General Electricity -> code: anta_eco_cityofantalya_generalelectiricbill_monthly
	-Pomp Electricity -> code: anta_eco_cityofantalya_waterpomps_monthly
	-Employers-> code: anta_eco_cityofantalya_operationemployeesalary_monthly
"""
""" Original files must be previously saved in folder temp"""
""" """



import os
import pandas as pd
import shutil
import uuid
from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"
logging.basicConfig(level=logging.INFO)
#codes and corresponding columns in the datasheet
codes= [['anta_eco_cityofantalya_visitorticket_monthly','Visitor Ticket','Entrance Fee'],
['anta_eco_citiofantalya_otopark_monthly','Otopark Ticket','Parking Fee'],
['anta_eco_cityofantalya_generalelectiricbill_monthly','General Electricity'],['anta_eco_cityofantalya_waterpomps_monthly','Pomp Electricity'],
['anta_eco_cityofantalya_operationemployeesalary_monthly','Employers']]

l_temp_path = './temp/'
l_final_path = './data/'

xlfname = 'gelir-gider.xlsx' 


class anta_eco_several_codes(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (header = 1,usecols='A:J')

		#remove index columns
		df_data.reset_index(inplace = True)

		
		df_data.rename(columns={df_data.columns[0]:'Year',df_data.columns[1]:'Month'},inplace=True)
		#df.index = pd.Series(df.index).fillna(method='ffill')

		df_data.Year = pd.Series(df_data.Year).fillna(method='ffill')

		#First cleaning of sensor data column names

		df_data.columns = df_data.columns.str.replace(r"\(.*\)","")#remove all braces and data inside
		print(len(df_data.columns))
		print (df_data.columns.tolist)

		print (len(df_data))


		#remove the rows with TOTAL
		df_data = df_data[df_data.Year!='TOPLAM'] 

		#df_data=df_data[~df_data.Year.str.contains("TOPLAM")]

		#df_data = df_data[df_data['Year'].isin(['TOPLAM'])] 

		print (len(df_data))


		df_data['Month']=df_data['Month'].replace({'Ocak':'January','Şubat':'February','Mart':'March','Nisan':'April','Mayıs':'May','Haziran':'June','Temmuz':'July','Ağustos':'August','Eylül':'September','Ekim':'October','Kasım':'November','Aralık':'December'})
		

		#df_data.drop(df_data.tail(1).index,inplace=True)

		#get only the columns of interest
		#df_data_clean = df_data[['ID','Height well ', 'Height ground level ', 'Location','X ','Y ', 'X-coordinate ','Y-coordinate ']].copy()


		#Any date to reformat?	
		#df_data_clean['Date'] = pd.to_datetime(df_merge_clean['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

		#df_data_clean.rename(columns={'Peil_cor2':'Water level','X ':'Longitude','Y ':'Latitude','Height well ':'Height well','X-coordinate ':'X','Y-coordinate ':'Y'},inplace=True)

		for item in codes:
		#save
		
			if len(item)>2 :
				df_data_filter = df_data[['Year','Month',item[1],item[2]]]

			else:

				df_data_filter = df_data[['Year','Month',item[1]]]

			df_data_filter.rename(columns={'Otopark Ticket':'tickets_number','Parking Fee':'fee_revenue','Visitor Ticket':'tickets_number','Entrance Fee':'fee_revenue','Pomp Electricity':'waterpomp_electric_bill','General Electricity':'electric_bill','Employers':'employee_salary','Shop Rent':'shop_rent'},inplace=True)
			
			outerdir = l_final_path
			if not os.path.exists(outerdir):
				os.mkdir(outerdir)
			outdir = outerdir+'/'+item[0]
			if not os.path.exists(outdir):
				os.mkdir(outdir)

			csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
			print ('writing to folder '+item[0])
			fullname = os.path.join(outdir, csvfile)

			df_data_filter.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)

	def producer(self):
		""" This function sends data to kafka bus"""
		producer = KafkaProducer(bootstrap_servers=['HOST_IP:PORT'], api_version=(2, 2, 1))
		topic = "ANTA_ECO_CITYOFANTALYA_VISITORTICKET_MONTHLY_DATA_INGESTION"
		topic_1 = "ANTA_ECO_CITIOFANTALYA_OTOPARK_MONTHLY_DATA_INGESTION"
		topic_2 = "ANTA_ECO_CITYOFANTALYA_GENERALELECTIRICBILL_MONTHLY_DATA_INGESTION"
		topic_3 = "ANTA_ECO_CITYOFANTALYA_WATERPOMPS_MONTHLY_DATA_INGESTION"
		topic_4 = "ANTA_ECO_CITYOFANTALYA_OPERATIONEMPLOYEESALARY_MONTHLY"
		producer.send(topic, b'Antalya visitor ticketing one-time data ingested to HDFS').get(timeout=30)
		producer.send(topic_1, b'Antalya otopark one-time data ingested to HDFS	').get(timeout=30)
		producer.send(topic_2, b'Antalya electricity one-time data ingested to HDFS	').get(timeout=30)
		producer.send(topic_3, b'Antalya water pump one-time data ingested to HDFS').get(timeout=30)
		producer.send(topic_4, b'Antalya employee salary one-time data ingested to HDFS').get(timeout=30)
			

if __name__ == '__main__':
	a = anta_eco_several_codes()
	a.parse_file()
	a.producer()