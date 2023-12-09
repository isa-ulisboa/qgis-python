import geopandas as gpd
import pandas as pd
from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from PyQt5.QtWidgets import QAction # necessary to save the project

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py  <---- just one function: my_zoom_to_layer
#    |---- input_subfolder
#         |---- fn_caop
#         |---- fn_prod
#         |---- fn_codes
#   |---- output_subfolder 
#         |---- fn_out <----- to be created

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# data folders and file names
input_subfolder='input'
output_subfolder='output'
fn_caop= 'Cont_Conc_CAOP2022.shp' # map of counties with county code
fn_prod = 'vinho_branco.csv' # simple csv table with county names
fn_codes='cod_municipios_pordata.csv' # simple csv table with county codes and names (to merge the other two tables)

# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

# add layer the usual way, using PyQGIS
QgsProject.instance().clear()
# the simplest way to read a tif file: read raster with iface, which creates QgsRasterLayer instance
# add basemap
iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
# load counties
fn = my_folder / input_subfolder / fn_caop
caop=iface.addVectorLayer(str(fn),'CAOP','ogr')
# zoom to layer
my_zoom_to_layer(caop.name())

####################################### read tables with geopandas and pandas
# read vector file with geopandas 
fn = my_folder / input_subfolder / fn_caop
gdf=gpd.read_file(fn, encoding='utf-8')
print(gdf.dtypes)

# Read csv files (note that encoding is ISO-8859-1)
fn = my_folder / input_subfolder / fn_prod
prod=pd.read_csv(fn,sep=';',encoding='ISO-8859-1')
print(prod.dtypes)

fn = my_folder / input_subfolder / fn_codes
codes=pd.read_csv(fn,sep=';',encoding='ISO-8859-1')
print(codes.dtypes)
codes.describe()

####################################### merge tables

# Convert type so both columns have the same type 'str' and 4 symbols (padded with 0) before merging
gdf['DICO']=gdf['DICO'].astype(str).str.pad(4, side='left', fillchar='0')
codes['DTCC']=codes['DTCC'].astype(str).str.pad(4, side='left', fillchar='0')

# Merge CAOP with codes
gdf_codes=gdf.merge(codes,left_on='DICO', right_on='DTCC', how='left')
print(gdf_codes.dtypes)

# Merge CAOP_codes with prod
gdf_prod=gdf_codes.merge(prod,on='municipio_pordata')
print(gdf_prod.dtypes)

################################################ export result as shapefile

# Select subset of columns
gdf_prod=gdf_prod[['geometry','DICO','Concelho','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']]

# Two possibilities:
# 1) create QGIS vector (T26) layer and save as shapefile, e.g. processing.run("native:savefeatures", {'INPUT':mylayer, 'OUTPUT':fn})
# 2) save geopandas as shapefile (new):

fn_out = 'white_wine_production.shp'
fn = my_folder / output_subfolder / fn_out
gdf_prod.to_file(fn,encoding='utf-8')

# load layer to QGIS
mylayer=iface.addVectorLayer(str(fn),'Wine production','ogr')


