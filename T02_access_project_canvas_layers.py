# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Asian hornet data (STOPvespa 2023 data from ICNF)

# Assumption: there is already an open project in QGIS

# Goals of this script:
# access project and read project
# access my canvas
# list layers in canvas or project
# access layer by name
# change layer name
# zoom to layer
# read layer id
# toggle layer visibility

import os
import sys

# Create variable that points to project
myproject=QgsProject.instance()

# Print project home path
project_path=myproject.homePath()
print(project_path)

# One can access to canvas
mycanvas=iface.mapCanvas()

# And operate on canvas, e.g. Zoom to full extent
mycanvas.zoomToFullExtent()
mycanvas.refresh()

# Layers in canvas
# Try toggle visibility and see what changes on mycanvas.layers()
print('Layers in mycanvas: ',mycanvas.layers()) # list
print(mycanvas.currentLayer())  # Can be None if no layer is selected

# Layers in project
# Try toggle visibility and see what changes on myproject.layers()
print('Layers in myproject: ',myproject.mapLayers()) # dictionary

# zoom to layer
# Access layer in project if it exists
layer_name='Cont_Conc_CAOP2022'
mylayers=myproject.mapLayersByName(layer_name)
# mylayer is the first in the returned list
mylayer=mylayers[0]
# Note: it would be more prudent to check that the list is not empty with `if mylayers:´
# Determine extent
extent = mylayer.extent()
mycanvas.setExtent(extent)
mycanvas.refresh()

# Access layer in project if it exists
# Now for the other layer
layer_name='STOPVespa_2023_simplified'
mylayers=myproject.mapLayersByName(layer_name)
mylayer=mylayers[0]

# get the layer id
print(mylayer.id())

# rename mylayer
new_layer_name='STOPVespa_2023'
mylayer.setName(new_layer_name)
# the id does not change
print(mylayer.id())
    
# Identify layer and make it not visible
layer_name='OpenStreetMap'
mylayers=myproject.mapLayersByName(layer_name)
# Note: it would be more prudent to check that the list is not empty with if mylayers:
# mylayer is the first in the returned list
mylayer=mylayers[0]
# get the layer id
mylayer_id=mylayer.id()
# access layerTree
root=myproject.layerTreeRoot() # QgsLayerTree
# identify tree layer: QgsLayerTreeLayer
mytreelayer=root.findLayer(mylayer_id) # QgsLayerTreeLayer
# make it not visible
mytreelayer.setItemVisibilityChecked(False)
# make it visible again
mytreelayer.setItemVisibilityChecked(True)
    
