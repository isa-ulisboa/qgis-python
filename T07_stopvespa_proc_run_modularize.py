# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Asian hornet data (STOPvespa 2023 data from ICNF)

# Assumption: there is already an open project in QGIS

# Goals of this script:
# in general, we want to improve T02 in order to:
# use paths relative to project file location
# use memory layers for intermediate results
# save final layer as file
# use a variable that defines the diameter threshold

from pathlib import Path 
#A file or directory path consists of different parts. When you use pathlib, these parts are conveniently available as properties. Basic examples include:
#    .name: The filename without any directory
#    .stem: The filename without the file extension
#    .suffix: The file extension
#    .anchor: The part of the path before the directories
#    .parent: The directory containing the file, or the parent directory if the path is a directory
#

################################################## Constants
D=25 # threshold nest diameter 
my_expression = ' "diameter" > '+str(D)

# Layer names:
ln_caop='Cont_Conc_CAOP2022' # CAOP 
ln_vespa='STOPVespa_2023_simplified' # STOPvespa

# project and data folders
input_subfolder='input'
output_subfolder='output'

# Working directory:
# |----myfolder
#    |---- project_name.qgz
#    |---- input
#         |---- fn_caop
#         |---- fn_vespa
#    |---- output

################################################# Functions

def create_path(path_as_list,prefix,suffix,ext="shp"):
    """ 
    function to create the file name; if the directory does not exist it will be created
    inputs:
    list of paths 
    filename prefix
    filename suffix
    filename extension (default: shp)
    output: full path
    """
    filename = prefix+'_'+suffix+'.'+ext
    # return Path(*path_as_list) / filename
    mysubfolder=Path(*path_as_list)
    # Check if folder exists and create folder otherwise
    if not mysubfolder.exists():
        mysubfolder.mkdir(parents=True)
    return Path(*path_as_list) / filename


def my_processing_run(operation,ln_input,dict_params,layer_name):
    """ function to execute processing.run from a list of parameters
    it creates a temporary output (in memory)
    dict_params: dictionary with operation parameters except 'INPUT' and 'OUTPUT'
    layer_name: name for the output layer
    output: output QgsVectorLayer"""
    dict_params['INPUT']=ln_input
    dict_params['OUTPUT']=QgsProcessing.TEMPORARY_OUTPUT
    mylayer=processing.run(operation,dict_params)['OUTPUT']
    if isinstance(mylayer,QgsVectorLayer):
        mylayer.setName(layer_name)
        myproject.addMapLayer(mylayer)
        return mylayer

def my_export_layer_as_file(mylayer,fn):
    """ # function to save QgsVectorLayer as file """
    if isinstance(mylayer,QgsVectorLayer):
        # select all features
        mylayer.selectAll()
        # file name has to be a string
        processing.run("native:saveselectedfeatures", {'INPUT':mylayer, 'OUTPUT':str(fn)})
        # unselect
        mylayer.removeSelection()

##################################################
# main
##################################################
# 1. Access project and identify layers
myproject=QgsProject.instance()
# path to project folder
myfolder=Path(myproject.homePath())

#################################################
# 2. create QgsVectorLayer from layer name
# CAOP
caop=myproject.mapLayersByName(ln_caop)[0]
# STOPvespa
vespa=myproject.mapLayersByName(ln_vespa)[0]

##################################################
# 3. Spatial analysis with processing.run()

# 3.1 Extract by expression
params={'EXPRESSION': my_expression}
ln='diameter_larger_than_'+str(D)
vespa_D=my_processing_run("native:extractbyexpression", vespa, params, ln)

# 3.2 Extract by location
params={'PREDICATE':[1], 'INTERSECT':vespa_D,}
ln='counties_with_nests_larger_than_'+str(D)
conc_D=my_processing_run("native:extractbylocation", caop, params, ln)

# 3.3 (optional) remove layer vespa_D from project
if vespa_D in myproject.mapLayers().values():
    myproject.removeMapLayer(vespa_D.id())

####################################################
# 4. Export result to shapefile
    
# 4.1
# create new path to output file
fn=create_path([myfolder,output_subfolder],'CAOP',str(round(D)),ext="shp")
# export to file
my_export_layer_as_file(conc_D,fn) 

# 4.2. (optional) remove layer
if conc_D in myproject.mapLayers().values(): 
    myproject.removeMapLayer(conc_D.id())