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

##################################################### Change symbology with shader
stats = rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
min = stats.minimumValue
max = stats.maximumValue
fcn = QgsColorRampShader()
fcn.setColorRampType(QgsColorRampShader.Interpolated) # Interpolated, Discrete, or Exact
lst = [ QgsColorRampShader.ColorRampItem(min, QColor("red")),
        QgsColorRampShader.ColorRampItem(min+(max-min)*0.2, QColor("orange")),
        QgsColorRampShader.ColorRampItem(min+(max-min)*0.4, QColor("yellow")),
        QgsColorRampShader.ColorRampItem(min+(max-min)*0.6, QColor("green")),
        QgsColorRampShader.ColorRampItem(max, QColor("blue"))]
fcn.setColorRampItemList(lst)
shader = QgsRasterShader()
shader.setRasterShaderFunction(fcn)
# set renderer and refresh
renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader) # <--- QgsSingleBandPseudoColorRenderer
rlayer.setRenderer(renderer)
rlayer.triggerRepaint()
