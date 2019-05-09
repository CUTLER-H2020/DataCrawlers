# -*- coding utf-8 -*-
""" -This scripts converts the .shp shapefiles to GeoJSON format for further usage"""
""" -The available content in .shp file is extracted to get the fields name and respective data"""
""" - The file is stored in GeoJSON in the storage directory"""
import shapefile
import  pandas as pd
from pandas.io.json import json_normalize
__author__ = "Hassan Mehmood"
__email__ = "hassan.mehmood@oulu.fi"
__origin__ = "UbiComp - University of Oulu"

def shapeConvertor():
    """This function extracts the data from the shapefile and converts it GeoJson for further usage"""
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 2000)
    reader = shapefile.Reader("") # Add path of the file to read the content of .shp file
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
       atr = dict(zip(field_names, sr.record))
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr))
    df = json_normalize(buffer) #Removes nested structure
    path = "" # Storage directory for converted GeoJSON
    filname = path + "Name_of_file" + ".json"
    df.to_json(filname)

shapeConvertor()