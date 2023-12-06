#from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from PyQt5.QtWidgets import QAction # necessary to save the project

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- input_subfolder
#         |---- fn_caop
#         |---- fn_s2
#   |---- output_subfolder 

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# project, data folders and file names
project_name='S2_Alcoutim'
input_subfolder='input'
output_subfolder='output'
fn_caop= 'Cont_Conc_CAOP2022.shp'
fn_s2='S2A-T29SNB-B2348-2021-8-22.tif'
ln='S2SR-B2348'
# bands of fn (in order):
band_names=['band2','band3','band4','band8']
# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

# my color composite
myRGB={'R':'band8', 'G':'band4','B':'band3'}
K=2 # number of standard deviations

##############################################################
QgsProject.instance().clear()
# the simplest way to read a tif file: read raster with iface, which creates QgsRasterLayer instance
# add basemap
iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
# load counties
fn = my_folder / input_subfolder / fn_caop
caop=iface.addVectorLayer(str(fn),'CAOP','ogr')
# load raster
fn = my_folder / input_subfolder / fn_s2
rlayer=iface.addRasterLayer(str(fn),ln,'gdal')
# zoom to layer
my_zoom_to_layer(rlayer.name())

############################################## information about raster layer
# get the total band count of the raster
nbands=rlayer.bandCount()

# get the band name 
for idx in range(0,nbands): 
    print('QGIS band layer: ', rlayer.bandName(idx+1)) 
    print('S2 band: ', band_names[idx]) 

# size and extent
print(f"Width: {rlayer.width()} px")
print(f"Height: {rlayer.height()} px")
print(f"Extent: {rlayer.extent().toString()}") # rlayer.extent() is QgsRectangle

# To get the minimum and maximum values of a single-band raster, we can access its data provider’s band statistics:
for idx in range(0,nbands): 
    stats = rlayer.dataProvider().bandStatistics(idx+1)
    print(f"{rlayer.bandName(idx+1)} Min value: {stats.minimumValue}")
    print(f"{rlayer.bandName(idx+1)} Max value: {stats.maximumValue}")

################################################### renderer
# renderer
# When a raster layer is loaded, it gets a default renderer based on its type. 
# It can be altered either in the layer properties or programmatically.
# get the raster type: 0 = GrayOrUndefined (single band), 1 = Palette (single band), 2 = Multiband
print(rlayer.rasterType())
# To query the current renderer:
print(rlayer.renderer().type())

###################################################################### create a renderer and plot the map
# create color composite
if False: # automatically determine band indices from RGB and band_names
    idxBandR=band_names.index(myRGB['R'])+1 # +1 since bands indices start at 1
    idxBandG=band_names.index(myRGB['G'])+1 # +1 since bands indices start at 1
    idxBandB=band_names.index(myRGB['B'])+1 # +1 since bands indices start at 1

# set color composite:
rlayer.renderer().setRedBand(4) # idxBandR
rlayer.renderer().setGreenBand(3) # idxBandG
rlayer.renderer().setBlueBand(2) # idxBandB
rlayer.triggerRepaint()
# refresh Layers panel
iface.layerTreeView().refreshLayerSymbology(rlayer.id())

######################################################################################
# simple way of stretching to min max in each band:
rlayer.setContrastEnhancement(QgsContrastEnhancement.StretchToMinimumMaximum)
rlayer.triggerRepaint()

######################################################################################
# more detailed approach: define min and max in each band, as mean-K*std and mean+K*std

for channel, band in myRGB.items():
    print(channel,band)
    # the band of the original multiband raster that corresponds to 'channel' (R,G, or B)
    idxBand=band_names.index(myRGB[channel])+1 # +1 since bands indices start at 1
    stats = rlayer.dataProvider().bandStatistics(idxBand)
    # Contrast Enhancement for each band separately
    band_type = rlayer.renderer().dataType(idxBand) 
    enhancement = QgsContrastEnhancement(band_type)
    # set minimum, maximum and stretch
    enhancement.setMaximumValue(stats.mean+K*stats.stdDev)
    enhancement.setMinimumValue(stats.mean-K*stats.stdDev)
    enhancement.setContrastEnhancementAlgorithm(QgsContrastEnhancement.StretchToMinimumMaximum)
    # update renderer
    if channel=='R': rlayer.renderer().setRedContrastEnhancement(enhancement)
    if channel=='G': rlayer.renderer().setGreenContrastEnhancement(enhancement)
    if channel=='B': rlayer.renderer().setBlueContrastEnhancement(enhancement)

# Set opacity
rlayer.renderer().setOpacity(0.9)
# Refresh
rlayer.triggerRepaint()
iface.layerTreeView().refreshLayerSymbology(rlayer.id())