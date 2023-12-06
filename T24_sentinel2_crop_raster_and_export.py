from osgeo import gdal, osr # raster input/output
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
#         |---- fn_s2_alcoutim  # <---- to be created

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

################################################################# crop raster layer
# processing.run

alcoutim=processing.run("native:extractbyexpression", 
{'INPUT':caop, 'EXPRESSION':' \"Concelho\" =  \'Alcoutim\' ',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']  # alcoutim is a vector layer
alcoutim.setName('Alcoutim')
QgsProject().instance().addMapLayer(alcoutim)

# Crop raster layer with vector mask
fn_crop= processing.run("gdal:cliprasterbymasklayer", 
{'INPUT':rlayer,'MASK':alcoutim,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']  # fn_crop is a string !
# load temporary file
crop_layer=iface.addRasterLayer(fn_crop,'S2 Alcoutim', 'gdal')  

############################################# set nodata value equal to 0 (see T20)
provider = crop_layer.dataProvider()
for i in range(4):
    provider.setNoDataValue(i+1, 0) # band, nodata value

# refresh
crop_layer.triggerRepaint()

################################################## remove raster layers from project
QgsProject().instance().removeMapLayer(rlayer.id())
QgsProject().instance().removeMapLayer(caop.id())
iface.mapCanvas().refresh()

############################################### Save raster layer as geotiff file
fn_out = my_folder / output_subfolder / (ln + '_alcoutim.tif')
pipe = QgsRasterPipe()
pipe.set(crop_layer.dataProvider().clone())
file_writer = QgsRasterFileWriter(str(fn_out))
file_writer.writeRaster(pipe, crop_layer.width(), crop_layer.height(), crop_layer.extent(), crop_layer.crs())