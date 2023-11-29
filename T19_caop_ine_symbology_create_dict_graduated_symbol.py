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

# categories for symbology
# my_legend={
#'Low production': (0,1000,QColor('dark green'), 0.3), # label, color, opacity
#'Middle production': (1000,20000,QColor('yellow'), 0.4), # label, color, opacity
#'High production': (20000,200000,QColor('red'), 0.5)
#}
# Instead of writing "by hand" a dictionary, as before, this script will use a function to create a dictionary
# The inputs for the function are:
# 1. a list with the values of the field my_attrib
my_attrib='Goat' 
# 2. colormap with attribute 'colors':  https://matplotlib.org/stable/users/explain/colors/colormaps.html
my_colormap= 'inferno' #'viridis'
# 3. a value between 0 and 1 for the opacity of the symbols
my_opacity=0.7
# 4. a string to add information to the classes in the legend, e.g. 'hl' for the units
my_units='hl'

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
    
    # Create legend dictionary
    my_legend=my_create_sturges_graduated_legend_dict(caop_ine,my_attrib,my_colormap,my_opacity,my_units)
    # Set layer's legend
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

def my_create_sturges_graduated_legend_dict(vlayer,attrib,colormap,myopacity,units):
    '''
        This function creates a dictionary to be used as input for setting up the legend
        the number of classes is given by Sturges rule
        # The inputs for the function are:
        # 1. the layer and one of its attributes
        # 2. the colormap from matplotlib, e.g. 'viridis'
        # 3. a value between 0 and 1 for the opacity of the symbols, e.g. 0.7
        # 4. a string to add information to the classes in the legend, e.g. 'hl' for the units
        
    '''
    from matplotlib.cm import get_cmap
    import numpy as np
    # determine what is the range of values for the legend
    idx = vlayer.fields().indexOf(attrib)
    values = list(vlayer.uniqueValues(idx)) # uniqueValues returns a "set"
    # determine min and max
    mymin=min(values)
    mymax=max(values)
    D={} # initializes dictionary
    count=0
    # number of classes as the logarithm of the number of observations (Sturges)
    N = int(1+np.ceil(np.log2(vlayer.featureCount())))
    breaks=np.linspace(0,mymax,num=N) # linspace divides interval in N parts
    # color using colormap defined in the header of the script
    mycolormap=get_cmap(colormap,N) # get N colors from colormap
    mycolors=mycolormap.colors*255 # numpy.ndarray
    for i in range(1,len(breaks)):
        # determine class minimum and maximum value
        if i==1: 
            classMin = 0
        else:
            classMin = classMax
        classMax = breaks[i]
        # define label
        mylabel = f'from {round(classMin)} to {round(classMax)} {units}'
        # choose count-th color from mycolors
        mycolor=mycolors[count]
        count +=1
        # create QColor object
        myQColor=QColor(mycolor[0],mycolor[1],mycolor[2]) #RGB
        # insert a new entry to the dictionary
        D[mylabel]= (classMin,classMax,myQColor,myopacity)
    return D # dictionary


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




