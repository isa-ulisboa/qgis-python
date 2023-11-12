# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Asian hornet data (STOPvespa 2023 data from ICNF)

# Goals of this script:
# create and save new project
# read shapefile as layer
# change layer encoding
# read csv as layer

import os
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from PyQt5.QtWidgets import QAction # necessary to save the project

########################################################################
# Constants
fn_caop='Cont_Conc_CAOP2022.shp' # CAOP shapefile
fn_vespa='STOPVespa_2023_simplified.csv'
# parameters for reading the csv file
d=';' # delimiter in the csv file
x='long'
y='lat'
crs='EPSG:4326'

# project and data folders
project_name='stopvespa'
input_subfolder='input'
output_subfolder='output'

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- project_name.qgz
#    |---- input
#         |---- fn_caop
#         |---- fn_vespa

# (A) If it's the script location:
# Find path to the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
myfolder=script_path.parent

# (B) If it's a given folder:
# Just define where your working directory is: myfolder= Path('C:/Users/.../caop_stopvespa')
# myfolder=Path(r'C:/Users/mlc/OneDrive - Universidade de Lisboa/Documents/Aulas-Cursos/cursos_curta_duracao/qgis_com_python_2023/shared_folder/T04_stopvespa_add_layers_with_python')

################################################################## Create project
# New project; clear project
myproject=QgsProject.instance() # QgsProject
myproject.clear() # Clear project 
myproject.setTitle(project_name)
project_file=str(myfolder/project_name)+'.qgz'
# Save project to file
myproject.write(project_file) # 

################################################################## Load layers
# https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/loadlayer.html#vector-layers

################################################################## Read vector layer (shapefile) and adapt encoding
# Firstly, create absolute file name of file to be read
fn = str(myfolder / input_subfolder / fn_caop)
print(fn)

# Simplest way of reading a shapefile, with iface
mylayer=iface.addVectorLayer(fn,'CAOP','ogr') # file name, layer name, data provider: 'ogr' for vector layers in general
print(mylayer.providerType())

# Equivalent, but in two steps
# 1. Create vector layer object
mylayer = QgsVectorLayer(fn,'CAOP_2','ogr') # would be prudent to check with `if not mylayer.isValid():´
# 2. add the layer to the project
myproject.addMapLayer(mylayer) #addMapLayer

# Note that CAOP does not have the correct encoding (check atribute table)
provider=mylayer.dataProvider()
if provider.encoding()!='UTF-8':
    mylayer.dataProvider().setEncoding('UTF-8')

################################################################# Read csv file with point coordinates
fn = str(myfolder / input_subfolder / fn_vespa) # solves the %20 problem when there are spaces in the path
print('fn',fn)

# Create uri (Uniform Resources Identifier)
# loading parameters -- suggestion: do it by hand and copy uri from layer information
params=f'?delimiter={d}&detectTypes=yes&xField={x}&yField={y}&crs={crs}'  # returns ?delimiter=;&detectTypes=yes&xField=lon&yField=lat&crs=EPSG:4326
# create uri as string
uri_file=(myfolder / input_subfolder / fn_vespa).as_uri()
uri=uri_file+params

# create and load layer
vlayer = QgsVectorLayer(uri, "locations", "delimitedtext")
myproject.addMapLayer(vlayer)

################################################################# Save project
# save project
if True: 
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()

