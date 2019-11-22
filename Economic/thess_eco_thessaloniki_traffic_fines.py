# -*- coding: utf-8 -*-
""" This code is open-sourced software licensed under the MIT license""" 
""" Copyright  2019 Marta Cortes, UbiComp - University of Oulu""" 
""" Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
""" 
""" 
DISCLAIMER
This code is used to crawl/parse data from several files from Thessaloniki Municipality. By downloading this code, you agree to contact the corresponding data provider and verify you are allowed to use (including, but not limited, crawl/parse/download/store/process) all data obtained from the data source.
""" 

""" Parse ods files into correct format in csv files. """
""" """
"""
	Structure

	Date - Address - Fine

	Example file is now in the drive : traffic_fines_data.ods
"""
""" """
""" Original file must be previously saved in folder temp/code_name"""
""" Name of ods file must be in the corresponding variable xlfdata"""
""" """
""" code: thess_eco_thessaloniki_traffic_fines """

import os
import pandas as pd
import shutil
import uuid
import ezodf

__author__ = "Marta Cortes"
__mail__ = "marta.cortes@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

code = "thess_eco_thessaloniki_traffic_fines"
xlfdata ='traffic_fines_data.ods'

l_temp_path = './temp/'
l_final_path = './data/'

class thess_eco_thessaloniki_traffic_fines (object):

	def __init__(self):
		self.local = True

	def parse_files(self):

		#first, parse sensor locations
		xlfdatalocation= l_temp_path+code+'/'+xlfdata

		"""OPEN ODS into dataframe. Code from stackoverflow"""
		doc = ezodf.opendoc(xlfdatalocation)#'some_odf_spreadsheet.ods')

		print("Spreadsheet contains %d sheet(s)." % len(doc.sheets))
		for sheet in doc.sheets:
		    print("-"*40)
		    print("   Sheet name : '%s'" % sheet.name)
		    print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )

		# convert the first sheet to a pandas.DataFrame
		sheet = doc.sheets[0]
		df_dict = {}
		for i, row in enumerate(sheet.rows()):
		    # row is a list of cells
		    # assume the header is on the first row
		    if i == 0:
		        # columns as lists in a dictionary
		        df_dict = {cell.value:[] for cell in row}
		        # create index for the column headers
		        col_index = {j:cell.value for j, cell in enumerate(row)}
		        continue
		    for j, cell in enumerate(row):
		        # use header instead of column index
		        df_dict[col_index[j]].append(cell.value)
		# and convert to a DataFrame
		df = pd.DataFrame(df_dict)
		#renaming columns
		df.rename(columns={'DATE':'Date', 'ADDRESS':'Address', 'FINE':'Revenue'},inplace=True)
		#Date format
		#df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%dT%H:%M+01')
		#Delete rows that have no date (they represent total value)
		df1=df.dropna(subset=['Date'])
		outerdir = l_final_path
		if not os.path.exists(outerdir):
			os.mkdir(outerdir)
		outdir = outerdir+'/'+code
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		outdir2 = outdir+'/'+code+'_1'
		if not os.path.exists(outdir2):
			os.mkdir(outdir2)
		
		#df = df.append(df_tmp, ignore_index=True)
        #Write to the csv file. Note, put this out of the loop to write all the sheets in same csv file
		csvfile = str(uuid.uuid4()) + ".csv"#sheet+'.csv'
		print ('writing to folder '+code+'_1')
		fullname = os.path.join(outdir2, csvfile)
		df1.to_csv(fullname, mode='w', encoding='utf-8-sig', index=False)


if __name__ == '__main__':
	a = thess_eco_thessaloniki_traffic_fines ()
	a.parse_files()	
