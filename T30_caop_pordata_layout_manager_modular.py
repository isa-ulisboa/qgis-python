from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from qgis.PyQt import QtGui
from PyQt5.QtGui import QFont
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import jenkspy

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py  <-- include several functions for the layout
#    |---- input_subfolder
#         |---- fn_wine  <-- created in T27
#    |---- output_subfolder 
#         |---- ...pdf <----- to be created
#         |---- ...png 

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# data folders and file names
input_subfolder='input'
output_subfolder='output'
fn_wine= 'white_wine_production.shp' # map of counties with white wine production from 2009 to 2019
# output file prefix
fn_export='white_wine_production_'

# The inputs for the function are:
# 1. the year for the map and symbology
year_start='2009'
year_end='2019'
TITLE= 'White wine prodution' # Layer and layout names; layout title
N=10 # number of classes in Jenks legend
# 2. colormap with attribute 'colors':  https://matplotlib.org/stable/users/explain/colors/colormaps.html
my_colormap=  'inferno' # 'viridis' #
# 3. a value between 0 and 1 for the opacity of the symbols
my_opacity=0.5
# 4. a string to add information to the classes in the legend, e.g. 'hl' for the units
my_units='hl'

# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

# North arrow picture
fn_north_arrow = 'north-arrow-svgrepo-com.svg'

######################################################### load layers
# add layer the usual way, using PyQGIS
QgsProject.instance().clear()
# add basemap
iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")

# input file
fn = my_folder / input_subfolder / fn_wine

# create dictionary for graduated symbology based on Jenks' rule
dict_legend=my_create_jenks_symbology(fn,N,year_start,year_end,my_colormap,my_opacity,my_units)

# for each year:
# the layer with the year's symbology is going to be added to the project and to the layer tree
# then, a layout is created and map, legend, etc, are added to the layout
# the layout is exported as a png and/or pdf
# the layer is removed from the project and from the layer tree
for y in range(int(year_start), int(year_end)+1):
    year=str(y)
    print('year',year) # to track the execution
    layer_name=TITLE+' '+year
    layer=iface.addVectorLayer(str(fn),layer_name,'ogr')
    # zoom to layer
    my_zoom_to_layer(layer.name())
    # Set layer's symbology. The symbol for each feature depends on the year's production for the county
    my_set_graduated_legend(layer,year,dict_legend)
    ## Layer tree
    layerTree = QgsLayerTree() # necessary to add legend to layout
    layerTree.addLayer(layer)
    #############################################  Create and populate layout manager
    # adapted from https://opensourceoptions.com/pyqgis-create-and-print-a-map-layout-with-python/
    # see also https://github.com/epurpur/PyQGIS-Scripts/blob/master/CreateLayoutManagerAndExport.py
    layout_name=TITLE+' '+year
    manager,layout= my_create_layout_manager(layout_name)
    # add layer map to layout
    map=my_add_map_to_layout(layout,layer,20,20,120,180)
    # add scale bar: font 14; position 160, 180; 4 segments of 50 km
    my_add_scale_bar_to_layout(layout,map,14,160, 180,4,50)
    # add labels: text, font size, location (x,y) , box dimension (x,y)
    my_add_label_to_layout(layout,layer_name,20,10,5,100,20)
    my_add_label_to_layout(layout,'Source: PorData',16,160,100,100,20)
    # add north arrow (picture)
    # https://gis.stackexchange.com/questions/347026/adding-north-arrow-using-pyqgis
    fn_north = my_folder / fn_north_arrow # svg file
    my_add_picture_to_layout(layout,str(fn_north),120, 25,14,14)
    # add legend
    my_add_legend_to_layout(layout,layerTree,160,15)
    ######################################### save to pdf or png
    layout = manager.layoutByName(layout_name)
    exporter = QgsLayoutExporter(layout)
    #pdf
    fn_out = my_folder / output_subfolder / (fn_export+year)
    exporter.exportToPdf(str(fn_out.with_suffix(".pdf")), QgsLayoutExporter.PdfExportSettings())
    # png
    fn_out = my_folder / output_subfolder / (fn_export+year)
    exporter.exportToImage(str(fn_out.with_suffix(".png")), QgsLayoutExporter.ImageExportSettings())
    ## remove current layer from QgsLayerTree and from the Layers Panel
    layerTree.removeLayer(layer)
    QgsProject().instance().removeMapLayer(layer.id())

