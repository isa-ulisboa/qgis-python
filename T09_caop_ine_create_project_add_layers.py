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


# Working directory:
# |----myfolder
#    |---- script_file.py
#    |---- project_name.qgz  <--- to be created
#    |---- input_subfolder
#         |---- fn_caop
#         |---- fn_ine
#   |---- output_subfolder

# project and data folders
project_name='Milk_2020'
input_subfolder='input'
output_subfolder='output'

fn_caop='Cont_Conc_CAOP2022.shp' # CAOP shapefile
fn_ine='Milk_production_2020_INE.csv' # INE csv file
# parameters for reading the csv file
params_ine='?delimiter=;&detectTypes=yes&geomType=none'

# Determine path to working directory ("my_folder")

# (A) If it is the script location:
# Find path to the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# (B) If it is a given folder:
# Just define where your working directory is:
# my_folder= Path(r'C:/Users/.../working_directory')

# (C) if it is the path to an existent QGIS project file (most common choice if there is a project)
# my_project=QgsProject.instance()
# my_folder=Path(my_project.homePath())

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())


def main():
    # Create project and save to file
    my_project=my_create_project(my_folder,project_name)
    
    # load shapefile
    fn = my_folder / input_subfolder / fn_caop
    caop=my_add_vector_layer_from_shapefile(fn,'CAOP')
    
    # load csv
    fn = my_folder / input_subfolder / fn_ine
    ine = my_add_layer_from_csv(fn,'Milk production',params_ine)
    
    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()

main()
