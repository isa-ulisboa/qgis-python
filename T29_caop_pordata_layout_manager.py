from osgeo import gdal, osr # raster input/output
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from qgis.PyQt import QtGui
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import jenkspy

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py  <--  
#    |---- input_subfolder
#         |---- fn_wine  <-- created in T27
#   |---- output_subfolder 
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

year='2009'
year_start='2009'
year_end='2019'

# Instead of writing "by hand" a dictionary, as before, this script will use a function to create a dictionary
# The inputs for the function are:
# 1. the year for the map and symbology
year='2018'
year_start='2009'
year_end='2019'
# 2. colormap with attribute 'colors':  https://matplotlib.org/stable/users/explain/colors/colormaps.html
my_colormap=  'inferno' # 'viridis' #
# 3. a value between 0 and 1 for the opacity of the symbols
my_opacity=0.5
# 4. a string to add information to the classes in the legend, e.g. 'hl' for the units
my_units='hl'

# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

######################################################### load layers
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

############################################# Create symbology for the year

# 1. Read data with geopandas and select columns of production (years)
gdf=gpd.read_file(fn)
df_all = pd.DataFrame(gdf.drop(columns='geometry')) # drop geometries and convert to pandas dataframe
cols=df_all.columns[(df_all.columns >= year_start) & (df_all.columns <= year_end)]
df=df_all[cols]
# 2. Compute breaks for classes (Jenks)
# flatten dataframe to a single list of values
x= df.to_numpy().flatten()
# compute jenks breaks
breaks=jenkspy.jenks_breaks(x, n_classes=10)
# 3. create dictionary for legend
my_legend=my_create_graduated_legend_from_breaks_dict(breaks,my_colormap,my_opacity,my_units)
# Set layer's symbology (equal to T19), which depends on the year
my_set_graduated_legend(layer,year,my_legend)

#############################################  layout manager
# adapted from https://opensourceoptions.com/pyqgis-create-and-print-a-map-layout-with-python/
manager = QgsProject.instance().layoutManager()
layoutName = 'Wine production '+year
layouts_list = manager.printLayouts()
# remove any duplicate layouts
for layout in layouts_list:
    if layout.name() == layoutName:
        manager.removeLayout(layout)
layout = QgsPrintLayout(QgsProject.instance())
layout.initializeDefaults()
layout.setName(layoutName)
manager.addLayout(layout)

############################################## create map item in the layout
map = QgsLayoutItemMap(layout)
map.setRect(20, 20, 20, 20)
# set the map extent
ms = QgsMapSettings()
ms.setLayers([layer]) # set layers to be mapped
rect = QgsRectangle(ms.fullExtent())
rect.scale(1.7)
ms.setExtent(rect)
map.setExtent(rect)
map.setBackgroundColor(QColor(255, 255, 255, 0))
layout.addLayoutItem(map)
# resize and move
map.attemptMove(QgsLayoutPoint(20, 20, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(120, 180, QgsUnitTypes.LayoutMillimeters))

############################################# add legend
legend = QgsLayoutItemLegend(layout)
legend.setTitle("")
layerTree = QgsLayerTree()
layerTree.addLayer(layer)
legend.model().setRootGroup(layerTree)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(200, 15, QgsUnitTypes.LayoutMillimeters))

############################################ add scale bar
scalebar = QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Line Ticks Up')
scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
scalebar.setNumberOfSegments(4)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(50)
scalebar.setLinkedMap(map)
scalebar.setUnitLabel('km')
scalebar.setFont(QFont('Arial', 14))
scalebar.update()
layout.addLayoutItem(scalebar)
scalebar.attemptMove(QgsLayoutPoint(200, 190, QgsUnitTypes.LayoutMillimeters))

########################################## add title
title = QgsLayoutItemLabel(layout)
title.setText('White wine production for '+year)
title.setFont(QFont('Arial', 18))
title.adjustSizeToText()
title.update()
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))

########################################## add other text
other = QgsLayoutItemLabel(layout)
other.setText('Source: PorData')
other.setFont(QFont('Arial', 14))
other.adjustSizeToText()
other.update()
layout.addLayoutItem(other)
other.attemptMove(QgsLayoutPoint(200, 120, QgsUnitTypes.LayoutMillimeters))

######################################### save to pdf or png
layout = manager.layoutByName(layoutName)
exporter = QgsLayoutExporter(layout)

#pdf
fn = my_folder / output_subfolder / ('white_wine_production_'+year)
exporter.exportToPdf(str(fn.with_suffix(".pdf")), QgsLayoutExporter.PdfExportSettings())
# png
fn = my_folder / output_subfolder / ('white_wine_production_'+year)
exporter.exportToImage(str(fn.with_suffix(".png")), QgsLayoutExporter.ImageExportSettings())
