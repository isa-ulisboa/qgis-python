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
#         |---- fn_caop_ine_yes_no  <--- to be created

# project, data folders and file names
project_name='Milk_2020'
input_subfolder='input'
output_subfolder='output'
fn_caop_ine='CAOP_INE_milk_production.shp'
fn_caop_ine_yes_no='CAOP_INE_milk_production_yes_no.shp'

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

def main():
    # Create project and save to file
    my_create_project(my_folder,project_name)
    # load shapefile to memory
    fn= my_folder / input_subfolder / fn_caop_ine
    caop_ine=my_add_to_memory_vector_layer_from_shapefile(fn,'CAOP_INE')
    
    # check that the attribute 'Total' exists in the layer
    myattribs= caop_ine.dataProvider().fields().names()
    if 'Total' not in myattribs:
        return 0 # arbitrary value; just to exit main() if attribute does not exit
    
    # Create new categorized attribute 'produces' with values 'yes' or 'no'
    fld=QgsField('produces',QVariant.String)
    with edit(caop_ine):
        caop_ine.addAttribute(fld) 
        caop_ine.updateFields()
        for feat in caop_ine.getFeatures():
            if feat['Total'] == 0:
                feat['produces'] = 'no' 
            else:
                feat['produces'] = 'yes' 
            # “update-after-change”
            res=caop_ine.updateFeature(feat) # 'res' to be silent
    
    # save layer
    fn= my_folder / output_subfolder / fn_caop_ine_yes_no
    my_export_layer_as_file(caop_ine,fn)
    
    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()

    # return layer
    return caop_ine

if __name__ == '__console__':
    layer=main()

