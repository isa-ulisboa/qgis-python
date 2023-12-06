from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
# To access and plot raster values with rasterio
import rasterio 
from matplotlib import pyplot
import numpy as np

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py # just function my_zoom_to_layer
#    |---- input_subfolder
#         |---- fn_dem (.tif)
#   |---- output_subfolder 

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

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
src = rasterio.open(fn) # reads Path directly
print(src.meta) # meta data
print(src.read()) # values as array

# Create histogram 
from rasterio.plot import show_hist
show_hist(src, bins=50, alpha=0.3, label='m',  title="Histogram before new nodata")
src.close()

############################################# update nodata value and write to new file
# Data are read from input file, and the new data (with new nodata value) is written to a new file
new_nodata_value = -9999
fn_out = my_folder / output_subfolder / fn_dem

# Read the input raster dataset
with rasterio.open(fn) as src:
    profile = src.profile
    data = src.read()
    # Set the new nodata value in the profile
    profile.update(nodata=new_nodata_value)
    # Replace the current nodata value with the canonical nodata value np.nan
    data[data == src.nodata] == new_nodata_value
    # Write the output raster with the updated nodata value
    with rasterio.open(fn_out, "w", **profile) as dst:
        dst.write(data)

# redo histogram with new file
with rasterio.open(fn_out) as src: # reads Path directly
    # Create histogram 
    from rasterio.plot import show_hist
    show_hist(src, bins=50, alpha=0.3,label='m',  title="Histogram after new nodata")

# load new raster
rlayer=iface.addRasterLayer(str(fn_out),ln,'gdal')
