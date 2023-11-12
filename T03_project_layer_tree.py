# QGIS with Python
# ISA, ULIsboa, 2023
# Instructor: Manuel Campagnolo

# Goals of this script
# the ultimate goal is to be able to change the orders of layer in the Layers panel programatically
# to do this, one needs to access the QgsLayerTree instance (root)
# then, access and individual layer with a QgsLayerTreeLayer object
# finally, one needs to clone, insert and remove QgsLayerTreeLayer in the root

# references:
# https://gis.stackexchange.com/questions/351184/qgis-layer-tree-api-crashing-when-removing-layer
# https://www.lutraconsulting.co.uk/blog/2014/07/06/qgis-layer-tree-api-part-1/

# Access project (assumes that a project was open in QGIS)
myproject=QgsProject.instance()

######################################### Manage layers with QgsLayerTree
# To start working with the layer tree, we first need a reference to its root nade
root=myproject.layerTreeRoot() # QgsLayerTree

# The children are a list of QgsLayerTreeLayer (and possibly groups)
print(root.children())

######################################## Access layerTreeRoot layers
# First children (top layer)
child = root.children()[0] # QgsLayerTreeLayer
print(child.layer()) # QgsVectorLayer
print(child.name()) # string
print(child.parent()) # QgsLayerTree

############################################## Find layer by id
# Layers ids
root.findLayerIds() # List of strings (ids)
ids=root.findLayerIds()

# return the layer with the 1st id
mylayer=root.findLayer(ids[0]).layer() # QgsVectorLayer
print(mylayer)


##################################################################### Find layer by name
mylayer=myproject.mapLayersByName("STOPVespa_2023_simplified")[0]
mytreelayer=root.findLayer(mylayer.id()) # QgsLayerTreeLayer

# move QgsLayerTreeLayer position in QgsLayerTree
myclone = mytreelayer.clone()  # clone QgsLayerTreeLayer
root.insertChildNode(2, myclone) # insert clone at the desired position (0 is the top; -1 is the bottom position))
root.removeChildNode(mytreelayer) # remove original layertree to avoid duplicates

################################################################# Save project
# save project
if False: 
    iface.mainWindow().findChild( QAction, 'mActionSaveProject' ).trigger()

############################################################### Canvas and LayerTree
# from https://www.lutraconsulting.co.uk/blog/2015/01/30/qgis-layer-tree-api-part-3/
canvas = QgsMapCanvas()
bridge = QgsLayerTreeMapCanvasBridge(root, canvas)

canvas.show() # Creates second canvas
