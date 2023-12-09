from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from qgis.PyQt import QtGui
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import jenkspy
#The QMessageBox class provides a modal dialog for informing the user or for asking the user a question and receiving an answer
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel)

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py  <--  includes functions to determine the layer's symbology from a list of class breaaks
#    |---- input_subfolder
#         |---- fn_wine  <-- created in T27
#   |---- output_subfolder 

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# data folders and file names
input_subfolder='input'
output_subfolder='output'
fn_wine= 'white_wine_production.shp' # map of counties with white wine production from 2009 to 2019

# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

# access layerTree
root=QgsProject.instance().layerTreeRoot() # QgsLayerTree
parent=iface.mainWindow()
   
# Instead of writing "by hand" a dictionary, as before, this script will use a function to create a dictionary
# The inputs for the function are:
# 1. the year for the map and symbology
year='2018'
year_start='2009'
year_end='2019'
# 2. colormap with attribute 'colors':  https://matplotlib.org/stable/users/explain/colors/colormaps.html
my_colormap= 'inferno' #'viridis'
# 3. a value between 0 and 1 for the opacity of the symbols
my_opacity=0.7
# 4. a string to add information to the classes in the legend, e.g. 'hl' for the units
my_units='hl'

###############################################################  load layers
# add layer the usual way, using PyQGIS
QgsProject.instance().clear()
# the simplest way to read a tif file: read raster with iface, which creates QgsRasterLayer instance
# add basemap
iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
# load counties
fn = my_folder / input_subfolder / fn_wine
layer=iface.addVectorLayer(str(fn),'Wine production','ogr')
# zoom to layer
my_zoom_to_layer(layer.name())

############################################# Create symbology 
# 1. Read data with geopandas and select columns of production (years)
gdf=gpd.read_file(fn)
df_all = pd.DataFrame(gdf.drop(columns='geometry')) # drop geometries and convert to pandas dataframe
cols=df_all.columns[(df_all.columns >= year_start) & (df_all.columns <= year_end)] # select only year fields 
df=df_all[cols]
# 2. Compute breaks for classes (Jenks)
# flatten dataframe to a single list of values
x= df.to_numpy().flatten()
# compute jenks breaks
breaks=jenkspy.jenks_breaks(x, n_classes=10)
# 3. Set legend (see T19)
QgsProject().instance().removeMapLayer(layer.id())
# Create legend dictionary (adapted from T19) which is independent of the year
my_legend=my_create_graduated_legend_from_breaks_dict(breaks,my_colormap,my_opacity,my_units)
for year in range(2009,2020):
    year=str(year)
    print(year)
    layer=iface.addVectorLayer(str(fn),'Wine production'+' ' + year,'ogr')
    # Set layer's symbology (equal to T19), which depends on the year
    my_set_graduated_legend(layer,year,my_legend)
    # Turn off visibility (T02)
    # identify tree layer: QgsLayerTreeLayer
    mytreelayer=root.findLayer(layer.id()) # QgsLayerTreeLayer
    # make it not visible
    mytreelayer.setItemVisibilityChecked(False)

############################################### Visualize layers (T02) interactively
for year in range(2009,2020):
    # identify layer
    layer= QgsProject().instance().mapLayersByName('Wine production'+' ' + str(year))[0]
    # identify tree layer: QgsLayerTreeLayer
    mytreelayer=root.findLayer(layer.id()) # QgsLayerTreeLayer
    # set visibility (T02)
    mytreelayer.setItemVisibilityChecked(True)
    # interact with user (T17)
    if year < 2019:
        res=QMessageBox.question(parent,'Question', 'Year '+str(year)+': See following year?' )
        if res==QMessageBox.No:
            break
        mytreelayer.setItemVisibilityChecked(False)

