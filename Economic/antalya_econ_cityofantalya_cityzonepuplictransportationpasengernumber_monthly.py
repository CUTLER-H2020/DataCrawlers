# -*- coding: utf-8 -*-

""" Parse excel files into correct format in csv files. """
""" """
"""	Data are stored in an excel file named antalya_cutler_all_data_ (version 1).xlsx in different sheets """
""" Sheets names:

	- TRANSPORT_VML55A, TRANSPORT_VC56, TRANSPORT_KC35, TRANSPORT_KC35A, TRANSPORT_CV17A, TRANSPORT_MZ78, TRANSPORT_MK80, TRANSPORT_MK80A, TRANSPORT_VF66
"""
""" Original files must be previously saved in folder temp"""
""" """
""" code: ant_env_cityofant_gwl """



import os
import pandas as pd
import shutil
import uuid

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


code= 'anta_eco_citiofantalya_cityzonepuplictransportationpasengernumber_monthly' 

l_temp_path = './temp/'
l_final_path = './data/'
data_sheets = ['TRANSPORT_VML55A', 'TRANSPORT_VC56', 'TRANSPORT_KC35', 'TRANSPORT_KC35A', 'TRANSPORT_CV17A', 'TRANSPORT_MZ78','TRANSPORT_MK80', 'TRANSPORT_MK80A', 'TRANSPORT_VF66']

xlfname = 'antalya_cutler_all_data_ (version 1).xlsx'

class anta_eco_cityzonepuplictransportationpasengernumber_monthly(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)
		print ('opening file '+fileName)

		df_final = pd.DataFrame()

		for data_sheetn in data_sheets:
			#data into dataframe
			df_data = xl.parse (data_sheetn, header =1)

			print(len(df_data.columns))
			print(len(df_data))

			#remove index columns
			df_data.reset_index(inplace = True)

			#remove the last row
			df_data.drop(df_data.tail(2).index,inplace=True)

			#add reference to sheet name
			df_data['CODE'] = data_sheetn

		
			#First cleaning of sensor data column names 
			#df_data.columns = df_data.columns.str.replace(r"\(.*\)","")#remove all braces and data inside
			#print (df_data.columns.tolist)

			df_data_clean = df_data[['DATE', 'CODE','ZONE NAME', 'NUMBER  OF TOUR ', 'FREE1', 'FREE2', 'FREE3', 'TICKET', 'STUDENT', 'PERSON', 'KREDI KART PERSON ', 'TEACHER','RETRIED', 'S.KART INDIRIMLI', 'AIRPORT EMPLOYER', 'TAX AUDIT CARD','TOTAL SUM']].copy()

			#print (df_data_clean.count)

			print(len(df_data_clean.columns))
			print(len(df_data_clean))

			#print (df_data_clean.columns.tolist)

			df_final = df_final.append(df_data_clean)

			print(len(df_final.columns))
			print(len(df_final))
			#print (df_final.count)


		#Any date to reformat?	
		df_final['DATE'] = pd.to_datetime(df_final['DATE'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

		#RENAME COLUMNS
		df_final.rename(columns={'DATE':'Date', 'CODE':'Code','ZONE NAME':'Zone Name', 'NUMBER  OF TOUR ':'number_or_tour', 'FREE1':'free1', 'FREE2':'free2', 'FREE3':'free3', 'TICKET':'ticket', 'STUDENT':'student', 'PERSON':'person', 'KREDI KART PERSON ':'credit_card_person', 'TEACHER':'teacher','RETRIED':'retired', 'S.KART INDIRIMLI':'s_discount_card', 'AIRPORT EMPLOYER':'airport_employee', 'TAX AUDIT CARD':'tax_audir_card','TOTAL SUM':'total_sum'},inplace=True)


		#save
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		print ('writing to folder '+code)
		fullname = os.path.join(outdir, csvfile)

		df_final.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
	a = anta_eco_cityzonepuplictransportationpasengernumber_monthly()
	a.parse_file()	