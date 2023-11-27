# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Asian hornet data (STOPvespa 2023 data from ICNF)

# Goals of this script:
# export layer as shapefile

# assumption: there is a project

import os
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html

########################################################################
# Constants
fn_caop='Cont_Conc_CAOP2022.shp' # CAOP shapefile

# project and data folders
input_subfolder='input'
output_subfolder='output'

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- project_name.qgz
#    |---- input
#         |---- fn_caop
#         |---- fn_vespa

# Path to an existent QGIS project file (most common choice if there is a project)
myproject=QgsProject.instance()
myfolder=Path(myproject.homePath())

################################################################## project
myproject=QgsProject.instance() # QgsProject

################################################################## access layer
# Access layer in project if it exists
layer_name='Cont_Conc_CAOP2022'
mylayers=myproject.mapLayersByName(layer_name)
# mylayer is the first in the returned list
mylayer=mylayers[0]

# Note that CAOP does not have the correct encoding (check atribute table and properties)
provider=mylayer.dataProvider()
if provider.encoding()!='UTF-8':
    mylayer.dataProvider().setEncoding('UTF-8')
 

############################################################################### Export mylayer to shapefile
# Create path to output file
parent_path=(myfolder / output_subfolder / fn_caop).parent
new_path = parent_path / 'CAOP_1.shp'
fn_caop_1 = str(new_path)

#################################################### 1st alternative: QgsVectorFileWriter
# Driver name and encoding
options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = 'ESRI Shapefile'
options.fileEncoding = 'UTF-8'
# instance of QgsCoordinateTransformContext
context = QgsProject.instance().transformContext()
# write to file
QgsVectorFileWriter.writeAsVectorFormatV3(mylayer, fn_caop_1, context,options)

#################################################### 2nd alternative: Exporting with processing.run()
  
# create new path to output file
fn_caop_2 = str((myfolder / output_subfolder / fn_caop).parent / 'CAOP_2.shp')

# select all features of layer to export
processing.run("native:savefeatures", {'INPUT':mylayer, 'OUTPUT':fn_caop_2})

