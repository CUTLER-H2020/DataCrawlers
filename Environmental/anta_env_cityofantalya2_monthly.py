

# -*- coding: utf-8 -*-

""" Parse excel files into correct format in csv files. """
""" """
"""	Data are stored in an excel file named antalya_cutler_all_data_ (version 1).xlsx in different sheets """
""" Sheets names:
	- ENV_WATER_QUALTY_2012_2017
	Available fields
	TARİH	NKT	Sonuç Tarihi	"Toplam Koliformadet/100ml(a1)"	"Fekal Koliformadet/100mla2)"	"Fekal Streptokokadet/100ml(a3)"	"pHb1)"	"Renk, Koku Bulanıklık(b2)"
	"NH4-Nmg/L(c1)"	"SO4-2mg/l(c2)"	"NO2-1mg/l(c3)"	"NO3-2mg/l(c4)"	"Cl-1mg/l(c5)"	"BOİmg/l(d1)"	"T. Org. Krb (TOC) mg/L (h3)"	"KOİmg/l(d2)"	"TDSμs/cm(e1)"
	"Top. Nmg/l(f1)"	"Kjeldahl Azotu (TKN) mg/L(h1)"	"Top. Pmg/l(f2)"	"Cdμg/l(g1)"	"Crμg/l(g2)"	"Pbμg/l(g3)"	"Cuμg/l(g4)"	"Znμg/l(g5)"	"Feμg/l(g6)"
	"Alμg/l(g7)"	"Mnμg/l(g8)"	"Niμg/l(g9)"

	Transform to:
	Date	Latitude-Longitude	NOSonuç TarihiNO	"Toplam Koliformadet/100ml(a1)"	"Fekal Koliformadet/100mla2)"	"Fekal Streptokokadet/100ml(a3)"	"pHb1)"	"Renk, Koku Bulanıklık(b2)"
	"NH4-N"	"SO4-2"	"NO2-1"	"NO3-2"	"Cl-1"	"BOİ"	"T. Org. Krb (TOC)"	"KOİ"	"TDS"
	"Top. N"	"Kjeldahl Azotu (TKN)"	"Top. P"	"Cd)"	"Cr"	"Pb"	"Cu"	"Zn"	"Fe"
	"Al"	"Mn"	"Ni"

"""
""" Locations:
Duden Brook: 1 (36°57”854’ N, 30°43”266’ E), Duden Brook 2 (36°57”675’ N, 30°43”687’ E), Duden Brook 3 (36°55”862’ N, 30°39”733’ E), Duden Brook 4 (36°56”128’ N, 30°37”310’ E), 
Duden Brook 5 (36°57”210’ N, 30°37”652’ E), Duden Brook 6 (37°06”515’ N, 30°34”836’ E), Duden Brook 7 (36°54”112’ N, 30°46”012’ E), Duden Brook 8 (36°50”994’ N, 30°46”998’ E).

DD = (Seconds/3600) + (Minutes/60) + Degrees

"""
'''check  https://www.itilog.com for transformig location'''
""" Original files must (antalya_cutler_all_data_ (version 1).xlsx) be previously saved in folder temp"""
""" 
Folder for temporal file
l_temp_path = './temp/'
Folder for data
l_final_path = './data/'
"""
""" code: anta_env_cityofantalya2_monthly """


import string
import os
import pandas as pd
import shutil
import uuid

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"


code= 'anta_env_cityofantalya2_monthly' 

l_temp_path = './temp/'
l_final_path = './data/'
data_sheetn = 'ENV_WATER_QUALTY_2012_2017'

locations =[['D1','36°57”854’ N','30°43”266’ E'],['D2','36°57”675’ N','30°43”687’ E'],['D3','36°55”862’ N','30°39”733’ E'],['D4','36°56”128’ N','30°37”310’ E'],['D5','36°57”210’ N','30°37”652’ E'],['D6','37°06”515’ N','30°34”836’ E'],['D7','36°54”112’ N','30°46”012’ E'],['D8','36°50”994’ N','30°46”998’ E']]

xlfname = 'antalya_cutler_all_data_ (version 1).xlsx' 


class anta_env_cityofantalya2_monthly(object):

	def _init_(self):
		self.local = False

	def getDecimalValue(self,value):

		formula= value.split('’ ')
		print(formula[0])
		print(formula[1])
		if (formula[1] == 'N' or formula[1] == 'E'):
			parts = formula[0].split('”')
			Seconds=parts[1]
			print(parts[0])
			print(parts[1])
			parts2 = parts[0].split('°')
			Minutes = parts2[1]
			Degrees = parts2[0]
			print(parts2[0])
			print(parts2[1])
			return (int(Seconds)/3600) + (int(Minutes)/60) + int(Degrees)




	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (data_sheetn,header = 0)

		#remove index columns
		#df_data.reset_index(inplace = True)



		#First cleaning of sensor data column names

		df_data.columns = df_data.columns.str.replace(r"\(.*\)","")#remove all braces and data inside
		df_data.columns = df_data.columns.str.replace(r"\n.*","")#remove newline and what it is after it
		
		#clean data, to correct float
		df_data.replace(',', '.', regex=True,inplace=True)#rchange , per .
		
		print(len(df_data.columns))
		#print (df_data.columns.tolist)


		#Rename to comply with data models
		df_data.rename(columns={'TARİH':'Date','NKT':'sample_point_code','Sonuç Tarihi':'result_timestamp','Toplam Koliform':'conc_tot_colif','Fekal Koliform':'conc_fec_colif','Fekal Streptokok':'conc_fec_strept','pH':'pH','Renk, Koku Bulanıklık':'physical_characteristics'},inplace=True)
		df_data.rename(columns={'NH4-N':'NH4-N','SO4-2':'SO4-2','NO2-1':'NO2-1','NO3-2':'NO3-2','Cl-1':'Cl-1','BOİ':'conc_BOD','T. Org. Krb ':'conc_TOC','KOİ':'conc_COD','TDS':'TDS','Top. N':'conc_N','Kjeldahl Azotu ':'TKN','Top. P':'conc_P'},inplace=True)
		#not renaming
		#df_data.rename(columns={'Cd':'','Cr':'','Pb':'','Cu':'','Zn':'','Fe':'','Al':'','Mn':'','Ni':'','latitude':'','longitude':''},inplace=True)


		#save all in one file

		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		df_final = pd.DataFrame()
		for index, location in enumerate(locations):
	
			#all in one file
			outdir2 = outdir
			#subfolders
			#outdir2 = outdir+'/'+code+'_'+str(index+1)
			if not os.path.exists(outdir2):
				os.mkdir(outdir2)

			df_to_csv=df_data[df_data['point_id']==locations[index][0]]
			latd=locations[index][1]
			latd.split()
			lond=locations[index][2]
			lat = self.getDecimalValue(latd)
			lon = self.getDecimalValue(lond)
			print (lat)
			print (lon)
			df_to_csv['Latitude']= lat
			df_to_csv['Longitude']= lon
			#all in one file
			df_final = df_final.append(df_to_csv, ignore_index=True)
			#each one in one file
			#csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
			#print ('writing to folder '+code)
			#fullname = os.path.join(outdir2, csvfile)

			
		#all in one file
		csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		print ('writing to folder '+code)
		fullname = os.path.join(outdir2, csvfile)
		df_final.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)

		

if __name__ == '__main__':
	a = anta_env_cityofantalya2_monthly()
	a.parse_file()	