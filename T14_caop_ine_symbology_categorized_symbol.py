# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# CAOP (administrative units) and INE (milk production per county in Portugal), already joined

# Goals of this script:
# Determine vector layer symbology with categorized symbols

import os
from pathlib import Path # see https://docs.python.org/3/library/pathlib.html
from console.console import _console # necessary to obtain the folder of the python script
from PyQt5.QtWidgets import QAction # necessary to save the project

# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- my_functions.py
#    |---- project_name.qgz  <--- to be created
#    |---- input_subfolder
#         |---- fn_caop_ine
#   |---- output_subfolder

# project, data folders and file names
project_name='Milk_2020'
input_subfolder='input'
output_subfolder='output'
fn_caop_ine_yes_no='CAOP_INE_milk_production_yes_no.shp'
# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

def main():
    # Create project and save to file
    my_create_project_with_crs(my_folder,project_name,3763)
    # add basemap
    iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
    # set project CRS
    my_crs=QgsCoordinateReferenceSystem(3763)
    QgsProject.instance().setCrs(my_crs)
    # load shapefile to memory
    fn = my_folder / input_subfolder / fn_caop_ine_yes_no
    caop_ine=my_add_vector_layer_from_shapefile(fn,'CAOP_INE')
    # zoom to layer
    my_zoom_to_layer('CAOP_INE')
    
    # Define symbols for the layer
    mysymbol1=QgsSymbol.defaultSymbol(caop_ine.geometryType())
    mysymbol2=QgsSymbol.defaultSymbol(caop_ine.geometryType())
    # set colors, etc
    mysymbol1.setColor(QColor('light green'))
    mysymbol2.setColor(QColor('dark green'))
    # Create categories 
    cat1=QgsRendererCategory('no', mysymbol1, 'No milk production') # value, symbol, label
    cat2=QgsRendererCategory('yes', mysymbol2, 'Milk production')
    # Define renderer
    categories=[cat1,cat2]
    renderer = QgsCategorizedSymbolRenderer('produces', categories)
    # Set layer renderer
    caop_ine.setRenderer(renderer)
    # Refresh layer
    caop_ine.triggerRepaint()
    
    # exercise: try saving style as qml file with layer.saveNamedStyle(pathqml)
    
    # Refresh layer's symbology in Layer Tree
    iface.layerTreeView().refreshLayerSymbology(caop_ine.id())
    
    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()
    # return layer
    return caop_ine

if __name__ == '__console__':
    layer=main()

