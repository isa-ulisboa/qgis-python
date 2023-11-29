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
    # see possible ramps: print(QgsStyle().defaultStyle().colorRampNames())
    my_set_vector_graduated_ramp_legend(caop_ine,my_attrib,num_classes=5,ramp_name='Spectral')
    
    # (optional) Save layer in output folder with style as default
    fn = my_folder / output_subfolder / fn_caop_ine_yes_no
    my_export_layer_as_file(caop_ine,fn)
    fn_qml =  (my_folder / output_subfolder / fn_caop_ine_yes_no).with_suffix(".qml")
    caop_ine.saveNamedStyle(str(fn_qml))
    
    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()
    # return layer
    return caop_ine

def my_set_vector_graduated_ramp_legend(vlayer,value_field,num_classes,ramp_name):
    # https://gis.stackexchange.com/questions/342352/apply-a-color-ramp-to-vector-layer-using-pyqgis3
    classification_method = QgsClassificationJenks()
    #You can use any of these classification method classes:
    #QgsClassificationQuantile()
    #QgsClassificationEqualInterval()
    #QgsClassificationJenks()
    #QgsClassificationPrettyBreaks()
    #QgsClassificationLogarithmic()
    #QgsClassificationStandardDeviation()
    #
    # change format settings as necessary
    format = QgsRendererRangeLabelFormat()
    format.setFormat("%1 - %2")
    format.setPrecision(2)
    format.setTrimTrailingZeroes(True)
    # color ramp
    default_style = QgsStyle().defaultStyle()
    color_ramp = default_style.colorRamp(ramp_name)
    # renderer
    my_renderer = QgsGraduatedSymbolRenderer()
    my_renderer.setClassAttribute(value_field)
    my_renderer.setClassificationMethod(classification_method)
    my_renderer.setLabelFormat(format)
    my_renderer.updateClasses(vlayer, num_classes)
    my_renderer.updateColorRamp(color_ramp)
    # set renderer
    vlayer.setRenderer(my_renderer)
    # Refresh layer
    vlayer.triggerRepaint()

if __name__ == '__console__':
    layer=main()




