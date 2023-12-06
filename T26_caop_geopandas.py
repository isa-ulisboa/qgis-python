import geopandas as gpd
from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from PyQt5.QtWidgets import QAction # necessary to save the project

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- input_subfolder
#         |---- fn_caop
#   |---- output_subfolder 
#         |---- fn_alcoutim <---- a criar

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# data folders and file names
input_subfolder='input'
output_subfolder='output'
fn_caop= 'Cont_Conc_CAOP2022.shp'

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

####################################### geopandas
# read vector file with geopandas 
fn = my_folder / input_subfolder / fn_caop
gdf=gpd.read_file(fn, encoding='utf-8')

# List attributes (including geometry)
for fld in gdf.columns:
    print('Field name:',fld)

# Show geometry of the first feature
gdf.loc[0,'geometry']

# select by attribute
alcoutim=gdf[gdf['Concelho']=='Alcoutim']

################################################## convert geopandas into QGIS vector layer
# convert to layer using method to_json
mylayer = QgsVectorLayer(alcoutim.to_json(),'Alcoutim',"ogr")
QgsProject.instance().addMapLayer(mylayer)

################################################## change geometries
# see methods in https://geopandas.org/en/stable/docs/user_guide/geometric_manipulations.html
# Create map of rectangular envelopes of counties
gdf.geometry=gdf.geometry.envelope 

# convert to layer using method to_json
mylayer = QgsVectorLayer(gdf.to_json(),'Counties convex hulls',"ogr")
QgsProject.instance().addMapLayer(mylayer)