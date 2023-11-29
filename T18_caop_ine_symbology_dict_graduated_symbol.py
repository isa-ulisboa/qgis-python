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
#    |---- project_name.qgz  <--- to be created (optional)
#    |---- input_subfolder
#         |---- fn_caop_ine
#   |---- output_subfolder 
#         |---- fn_caop_ine    <--- to be created (optional)
#         |---- fn_caop_ine.qml

# project, data folders and file names
project_name='Milk_2020'
input_subfolder='input'
output_subfolder='output'
fn_caop_ine_yes_no='CAOP_INE_milk_production_yes_no.shp'
# basemap: OpenStreetMap
uri_OSM = 'type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0'

# graduated attribute to use for the legend
my_attrib='Total' # Total varies between 0 and 200000

# categories for symbology
my_legend={
'Low production': (0,1000,QColor('dark green'), 0.3), # label, color, opacity
'Middle production': (1000,20000,QColor('yellow'), 0.4), # label, color, opacity
'High production': (20000,200000,QColor('red'), 0.5)
}

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

def main():
    # Create project and save to file 
    my_create_project(my_folder,project_name)
    # add basemap
    iface.addRasterLayer(uri_OSM, "OpenStreetMap", "wms")
    # load shapefile to memory
    fn = my_folder / input_subfolder / fn_caop_ine_yes_no
    caop_ine=my_add_vector_layer_from_shapefile(fn,'CAOP_INE')
    # zoom to layer
    my_zoom_to_layer('CAOP_INE')
    
    # Create legend 
    my_set_graduated_legend(caop_ine,my_attrib,my_legend)
    
    # (optional) Save layer in output folder with style as default
    fn = my_folder / output_subfolder / fn_caop_ine_yes_no
    my_export_layer_as_file(caop_ine,fn)
    fn_qml =  (my_folder / output_subfolder / fn_caop_ine_yes_no).with_suffix(".qml")
    caop_ine.saveNamedStyle(str(fn_qml))
    
    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()
    # return layer
    return caop_ine

# creates graduated symbology from dictionary with structure as above
def my_set_graduated_legend(vlayer,attrib,dict):
    myRangeList=[]
    count=0
    for mylabel, (classMin,classMax, myQColor, myopacity) in dict.items():
        mySymbol = QgsSymbol.defaultSymbol(vlayer.geometryType())
        mySymbol.setColor(myQColor)
        mySymbol.setOpacity(myopacity)
        # For graduated symbols, there is a QgsClassificationRange object:
        myRange = QgsRendererRange(QgsClassificationRange(mylabel,classMin, classMax),mySymbol)
        myRangeList.append(myRange)
    # define Graduated Symbol renderer and pass it to mylayer
    my_renderer = QgsGraduatedSymbolRenderer(attrib, myRangeList)
     # set renderer
    vlayer.setRenderer(my_renderer)
    # Refresh layer
    vlayer.triggerRepaint()


if __name__ == '__console__':
    layer=main()




