# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# CAOP (administrative units) and INE (milk production per county in Portugal), already joined

# Goals of this script:
# Change vector layer symbology -- color, transparency, stoke_width, etc -- for single symbols

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
fn_caop_ine='CAOP_INE_milk_production.shp'
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
    # load shapefile
    fn = my_folder / input_subfolder / fn_caop_ine
    caop_ine=my_add_vector_layer_from_shapefile(fn,'CAOP_INE')
    
    # Change color and transparency -- single symbol
    caop_ine.renderer().symbol().setColor(QColor("gray"))
    caop_ine.renderer().symbol().setOpacity(0.3)
    caop_ine.triggerRepaint()
    # Refresh layer's symbology in Layer Tree
    iface.layerTreeView().refreshLayerSymbology(caop_ine.id())
    
    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()
    # return layer
    return caop_ine

if __name__ == '__console__':
    layer=main()

if False:
    ######################################################################### renderer
    # layer.renderer() gives access to the vector layers renderer object. 

    # There are different types of renderers: 
    # 1. Single Symbol (QgsSingleSymbolRenderer), 
    # 2. Categorized (QgsCategorizedSymbolRenderer), 
    # 3. Graduated (QgsGraduatedSymbolRenderer), ....
    print(layer.renderer().dump())

    # color
    mycolor=QColor('red')
    #or
    mycolor=QColor(12, 34, 56, 180)  #RGBA 0-255 (A is transparency between 0 to 255=opaque)
    #or
    mycolor=QColor('#ff0000')  #hexadecimal
    mycolor=QColor("red")
    layer.renderer().symbol().setColor(mycolor)
    # reset map
    layer.triggerRepaint()

    # transparency/opacity
    layer.renderer().symbol().setOpacity(0.9) # between 0 and 1=opaque
    layer.triggerRepaint()

    # other options in symbolLayer(0)
    dir(layer.renderer().symbol().symbolLayer(0)) 
    # examples
    layer.renderer().symbol().symbolLayer(0).setStrokeWidth(.8)
    layer.renderer().symbol().symbolLayer(0).setStrokeColor(QColor("gray"))
    layer.triggerRepaint()

    # Refresh layer's symbology in Layer Tree
    iface.layerTreeView().refreshLayerSymbology(layer.id())
