# -*- coding: utf-8 -*-

""" Parse excel file into correct format in csv files. """
""" """
"""	Data are stored in an excel file named Visitor numbers_cork.xlsx in a table"""
""" Columns names:
	-Date
	-Number of visitors
	-Number of visitors (pay)		

"""
""" Original files must be previously saved in folder temp"""
""" """



import os
import pandas as pd
import shutil
import uuid

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

#codes and corresponding columns in the datasheet
code='cork_eco_visitors_daily'

l_temp_path = './temp/'
l_final_path = './data/'

xlfname = 'Visitor numbers_cork.xlsx' 


class cork_soc_visitors_daily(object):

	def _init_(self):
		self.local = True

	def parse_file(self):
		fileName = l_temp_path+xlfname#
		xl = pd.ExcelFile(fileName)#read_excel(fileName)
		print ('opening file '+fileName)

		#data into dataframe
		df_data = xl.parse (header = 0,usecols='A:C')



		#print(len(df_data.columns))
		#print (df_data.columns.tolist)

		#print (len(df_data))

		#format date correctly
		df_data['Date'] = pd.to_datetime(df_data['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')


		#columns names to comply with data models	
		df_data.rename(columns={'Number of visitors':'number_visitors','Number of visitors (pay)':'number_of_psying_visitors'},inplace=True)

				
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		csvfile = str(uuid.uuid4()) + ".csv"
		print ('writing to folder '+code)
		fullname = os.path.join(outdir, csvfile)

		df_data.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)
			

if __name__ == '__main__':
	a = cork_soc_visitors_daily()
	a.parse_file()	