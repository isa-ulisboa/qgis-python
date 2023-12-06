from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from PyQt5.QtWidgets import QAction # necessary to save the project

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- input_subfolder
#         |---- fn_s2_alcoutim
#   |---- output_subfolder 

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# data folders and file names
input_subfolder='input'
output_subfolder='output'
fn_s2='S2SR-B2348_alcoutim.tif'
ln='S2SR-B2348'
# bands of fn (in order):
band_names=['band2','band3','band4','band8']
# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

##############################################################
QgsProject.instance().clear()
# the simplest way to read a tif file: read raster with iface, which creates QgsRasterLayer instance
# add basemap
iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
# load raster
fn = str(my_folder / input_subfolder / fn_s2)
crop_layer=iface.addRasterLayer(fn,ln,'gdal')
# zoom to layer
my_zoom_to_layer(crop_layer.name())

############################################# set nodata value equal to 0 (see T20)
provider = crop_layer.dataProvider()
for i in range(4):
    provider.setNoDataValue(i+1, 0) # band, nodata value
    
#################################################################
# processing.run

# Compute normalized difference between bands 2 (green) and 1 (blue)
fn_green_blue=processing.run("gdal:rastercalculator", 
{'INPUT_A': fn,'BAND_A':1,
'INPUT_B': fn,'BAND_B':2,
'FORMULA':'(B-A)/(B+A)',
'NO_DATA':-9999,
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
ndgb=iface.addRasterLayer(fn_green_blue,'NDGB', 'gdal')

# Compute mask (NDGB<0.07)
fn_mask=processing.run("gdal:rastercalculator", 
{'INPUT_A': fn_green_blue,'BAND_A':1,
'FORMULA':'A < 0.07',
'NO_DATA':-9999,
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
mask=iface.addRasterLayer(fn_mask,'Solar panels mask', 'gdal')

# polygonize mask to create polygons
fn_polys=processing.run("gdal:polygonize", 
{'INPUT':fn_mask,'BAND':1,'FIELD':'DN','EIGHT_CONNECTEDNESS':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
polys=iface.addVectorLayer(fn_polys,'Solar panels polys', 'ogr')

# compute area for each feature
polys_area=processing.run("qgis:exportaddgeometrycolumns", 
{'INPUT':polys,'CALC_METHOD':0,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
polys_area.setName('Solar panels w/ area')
QgsProject().instance().addMapLayer(polys_area)

# extract by expression
panels=processing.run("native:extractbyexpression", 
{'INPUT': polys_area,
'EXPRESSION':' "area" > 1000 AND "area" < 10000000',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

panels.setName('Solar panels')
QgsProject().instance().addMapLayer(panels)

# remove raster layers from project
QgsProject().instance().removeMapLayer(polys_area.id())
QgsProject().instance().removeMapLayer(polys.id())
QgsProject().instance().removeMapLayer(mask.id())
QgsProject().instance().removeMapLayer(ndgb.id())
iface.mapCanvas().refresh()

# zoom to layer
my_zoom_to_layer(panels.name())