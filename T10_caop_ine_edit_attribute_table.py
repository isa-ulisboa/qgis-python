# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Data sets: CAOP + INE (milk production per county)

# Goals of this script:
# Read layers, as before
# Edit layer to create a pair of keys for joining layers
# addAttribute
# getFeatures
# updateFeature

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

# Set my_folder to be the directory where the script is (https://stackoverflow.com/questions/65240051/finding-directory-of-python-script-from-qgis-python-console))
script_path = Path(_console.console.tabEditorWidget.currentWidget().path)
my_folder=script_path.parent

# load my_functions.py
exec(Path(my_folder/ "my_functions.py").read_text())

# main 
def main():
    # Create project and save to file
    my_create_project(my_folder,project_name)
    
    # load shapefile
    fn = my_folder / input_subfolder / fn_caop
    caop=my_add_vector_layer_from_shapefile(fn,'CAOP')
    
    # load csv
    fn = my_folder / input_subfolder / fn_ine
    ine=my_add_layer_from_csv(fn,'INE',params_ine)
    
    # add new attribute to INE to store the DICO code
    if "Add Attributes" in ine.dataProvider().capabilitiesString():
        # Add new attribute in layer ine with method addAttribute
        fld=QgsField("di_co",QVariant.String,len=10)
        with edit(ine):
           ine.addAttribute(fld) 
           ine.updateFields()
        ine.setName('INE_dico')
    else: 
        # use a Toolbox function to create a new layer with an attribute with NULL values
        params={'FIELD_NAME':'di_co','FIELD_TYPE':2,'FIELD_LENGTH':10,'FIELD_PRECISION':0}
        ine=my_processing_run("native:addfieldtoattributestable",ine,params,'INE_dico')
        print('INE capabilities',ine.dataProvider().capabilitiesString())

    # Edit layer to compute values for new attribute
    ine=my_INE_preprocessing(ine)

    # save project
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()
    
    # if one wants to return the layer
    return ine

def my_INE_preprocessing(layer):
    """
        Edit the vector layer and make some changes to it
        The goal is to compute the values of attribute di_co from the values of attribute NUTS_2013
        Only the values of NUTS_2013 with maximum length are of interest (those are the counties)
    """
    # 1st: determine maximum length of NUTS_2013
    maxDigits=0
    for f in layer.getFeatures():
        if len(f['NUTS_2013']) > maxDigits:
           maxDigits=len(f['NUTS_2013'])
    
    # 2nd: for those, compute and store new 4-digit code (last 4 digits) in di_co
    with edit(layer):
        for f in layer.getFeatures():
            if len(f['NUTS_2013']) == maxDigits:
                f['di_co'] = f['NUTS_2013'][-4:] # last 4 digits
                # “update-after-change”
                res=layer.updateFeature(f) # 'res' to be silent
    # return output layer
    return layer

if __name__ == '__console__':
    layer=main()



   
