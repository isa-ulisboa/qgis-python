from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
# To access and plot raster values with rasterio
import rasterio 
import matplotlib.pyplot as plt # for histogram with numpy
import numpy as np
#The QMessageBox class provides a modal dialog for informing the user or for asking the user a question and receiving an answer
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QLabel)
# sleep
import time

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py # just function my_zoom_to_layer
#    |---- input_subfolder
#         |---- fn_dem (.tif)
#   |---- output_subfolder 
#         |---- fn_dem (.tif) # to be created: where -9999 is set as nodata value

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# Necessary for QMessageBox
parent=iface.mainWindow()

# data folders and file names
input_subfolder='input'
output_subfolder='output'
fn_dem= 'dem_montejunto.tif'
ln='DEM'

# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

##############################################################
QgsProject.instance().clear()
# the simplest way to read a tif file: read raster with iface, which creates QgsRasterLayer instance
# add basemap
iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
# load raster
fn = my_folder / input_subfolder / fn_dem
rlayer=iface.addRasterLayer(str(fn),ln,'gdal')
# zoom to layer
my_zoom_to_layer(rlayer.name())

############################################## raster values with rasterio
with rasterio.open(fn) as src: # reads Path directly; does not need to be converted into string
    print(src.meta) # meta data
    # Create histogram 
    try:
        # build histogram with rasterio
        from rasterio.plot import show_hist
        show_hist(src, bins=50, alpha=0.3, label='m',  title="Histogram before new nodata")
    except: 
        # otherwise, use numpy and matplotlib
        nodata_value=src.nodata
        x=src.read() # returns numpy array
        x[x==nodata_value]=np.nan # replace by nan
        plt.hist(x.flatten(),bins=50)
        plt.title("Histogram before new nodata")
        plt.show()

# wait 3 seconds
time.sleep(3)

##################################################################  replace nodata by -9999
# Ask Yes/No question
res=QMessageBox.question(parent,'Question', 'Do you want to set -9999 as the nodata value?' )
if res==QMessageBox.No:
    raise ValueError('The end')

############################################# update nodata value, write to new file, and create new histogram
# Data are read from input file, and the new data (with new nodata value) is written to a new file
new_nodata_value = -9999
fn_out = my_folder / output_subfolder / fn_dem

# Read the input raster dataset, set new nodata value, and write raster to fn_out file
with rasterio.open(fn) as src:
    profile = src.profile
    data = src.read()
    # Set the new nodata value in the profile
    profile.update(nodata=new_nodata_value) 
    # Replace the current nodata value with new_nodata_value
    data[data == src.nodata] == new_nodata_value
    # Write the output raster with the updated nodata value
    with rasterio.open(fn_out, "w", **profile) as dst:
        dst.write(data)

# Create histogram from updated raster
with rasterio.open(fn_out) as src:
    print('nodata value is', src.nodata)
    try:
        # build histogram with rasterio
        from rasterio.plot import show_hist
        show_hist(src, bins=50, alpha=0.3, label='m',  title="Histogram after new nodata")
        src.close()
    except: 
        # otherwise, use numpy and matplotlib
        nodata_value=src.nodata
        x=src.read() # returns numpy array
        x[x==nodata_value]=np.nan # replace by nan
        plt.figure() # new figure
        plt.hist(x.flatten(),bins=50)
        plt.title("Histogram after new nodata")
        plt.show()

# load new raster
newlayer=iface.addRasterLayer(str(fn_out),ln,'gdal')

# remove previous layer
QgsProject().instance().removeMapLayer(rlayer.id())
iface.mapCanvas().refresh()
