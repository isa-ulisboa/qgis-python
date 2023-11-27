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

################################################## Constants
D=75 # threshold nest diameter 

# Layer names:
ln_caop='Cont_Conc_CAOP2022' # CAOP 
ln_vespa='STOPVespa_2023_simplified' # STOPvespa
# output file name
fn_caop_D='CAOP_'+str(D)+'.shp'

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

##################################################
# 1. Access project and identify layers
myproject=QgsProject.instance()
# path to project folder
myfolder=Path(myproject.homePath())

#################################################
# 2. create variables that point to input layers
# CAOP
mylayers=myproject.mapLayersByName(ln_caop)
# mylayer is the first in the returned list
caop=mylayers[0]

# STOPvespa
mylayers=myproject.mapLayersByName(ln_vespa)
# mylayer is the first in the returned list
vespa=mylayers[0]

##################################################
# 3. Spatial analysis with processing.run()

# 3.1 Extract by expression
vespa_D=processing.run("native:extractbyexpression", 
{'INPUT': vespa,
'EXPRESSION':' "diameter" > '+str(D),
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
vespa_D.setName('diameter_larger_than_'+str(D))
#myproject.addMapLayer(vespa_D) #addMapLayer

# 3.2 Extract by location
conc_D=processing.run("native:extractbylocation", 
{'INPUT':caop,
'PREDICATE':[1],
'INTERSECT':vespa_D,
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
conc_D.setName('counties_with_nests_larger_than_'+str(D))
#myproject.addMapLayer(conc_D) #addMapLayer

####################################################
# 4. Export result to shapefile
    
# create new path to output file
fn = str(myfolder / output_subfolder / fn_caop_D)

# select all features of layer to export
conc_D.selectAll()
# export layer to file named fn
processing.run("native:saveselectedfeatures", {'INPUT':conc_D, 'OUTPUT':fn})
conc_D.removeSelection()
