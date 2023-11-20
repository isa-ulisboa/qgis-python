# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Asian hornet data (STOPvespa 2023 data from ICNF)

# Assumption: there is already an open project in QGIS

import os
import sys
from pathlib import Path 
import matplotlib.pyplot as plt

####################################################### Load my_functions
# Access project directory (suppose the project is loaded in QGIS)
my_project=QgsProject.instance()
my_folder=Path(my_project.homePath())
# Access my_functions.py 
try: 
    #if my_functions.py is on a path other than my_folder, adapt
    exec(Path(my_folder / 'my_functions.py').read_text())
except:
    print('There is a problem reading project or my_functions')
    # just to stop and limit the error message
    sys.tracebacklimit = 0
    raise ValueError()

################################################## main
def main():
    # Define layer names and other constants
    ln_caop='Cont_Conc_CAOP2022' # CAOP 
    ln_caop_short='CAOP'
    ln_vespa='STOPVespa_2023_simplified' # STOPvespa
    # project and data folders
    input_subfolder='input'
    output_subfolder='output'
    # nest diameters
    thresholds=[75,100,150] #[0,10,25,50,75,100,150]

    # load CAOP: None if layer name does not exist
    caop=my_find_layer(ln_caop)
    # load STOPvespa
    vespa=my_find_layer(ln_vespa)
    # check that layers were well defined
    if caop is None or vespa is None:
        return 0 # 0 is an arbitrary value; we just want to exit the function main()

    # do the calculations
    counts=[]
    for D in thresholds:
        # compute number of counties
        my_expression = ' "diameter" > '+str(D)
        
        # Extract by expression
        params={'EXPRESSION': my_expression}
        ln='diameter_larger_than_'+str(D)
        vespa_D=my_processing_run("native:extractbyexpression", vespa, params, ln)
        
        # Extract by location
        params={'PREDICATE':[1], 'INTERSECT':vespa_D,}
        ln='counties_with_nests_larger_than_'+str(D)
        conc_D=my_processing_run("native:extractbylocation", caop, params, ln)
        
        # compute number of features
        N=conc_D.featureCount()
        
        # (optional) save conc_D as a new shapefile in output_subfolder
        fn_path=my_create_path_from_list([my_folder,output_subfolder],ln_caop_short,str(round(D)),ext="shp")
        my_export_layer_as_file(conc_D,str(fn_path))
        
        # (optional) remove layers from project
        my_remove_layer(vespa_D)
        my_remove_layer(conc_D)
        
        # append result to list
        counts.append(N)
    
    # Create plot
    plt.plot(thresholds, counts)
    # Add labels and title
    plt.xlabel("nests larger than")
    plt.ylabel("number of counties")
    plt.title("STOP vespa")
    # Show the graph
    plt.show()
    

if __name__ == '__console__':
    main()