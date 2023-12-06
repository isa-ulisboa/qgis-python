from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script

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

############################################## information about raster layer
# get the total band count of the raster
print(f"The number of bands is {rlayer.bandCount()}")

# size and extent
print(f"Width: {rlayer.width()} px")
print(f"Height: {rlayer.height()} px")
print(f"Extent: {rlayer.extent().toString()}") # rlayer.extent() is QgsRectangle

# dataProvider and no value
print(rlayer.dataProvider().sourceNoDataValue(1)) # band 1
type(rlayer.dataProvider().sourceNoDataValue(1))

############################################# set nodata value equal to -9999
provider = rlayer.dataProvider()
provider.setNoDataValue(1, -9999) # band, nodata value
rlayer.triggerRepaint()

############################################# reset min and max
renderer=rlayer.renderer()
myType = renderer.dataType(1)
myEnhancement = QgsContrastEnhancement(myType)
contrast_enhancement = QgsContrastEnhancement.StretchToMinimumMaximum
myEnhancement.setContrastEnhancementAlgorithm(contrast_enhancement,True)
# statistics for the raster layer
stats = provider.bandStatistics(1, QgsRasterBandStats.All, rlayer.extent(), 0)
# setup min and max
min = stats.minimumValue
max = stats.maximumValue
myEnhancement.setMinimumValue(min)   #Set the minimum value you want
myEnhancement.setMaximumValue(max)   #Put the maximum value you want 
# set renderer and refresh
rlayer.renderer().setContrastEnhancement(myEnhancement)
rlayer.triggerRepaint()
