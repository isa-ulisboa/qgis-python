def my_project_path(my_project):
    """
        output: Path to the folder where the project is
    """
    # If there is a project, mufolder will be location of the project
    if my_project.fileName()!='':
        print('project', Path(my_project.fileName()).stem ,  'loaded')
        return Path(my_project.homePath())
    else:
        print('No project available')
        return 0 # exits main if there is no project available

def my_find_layer(ln):
    """
        tries to find a project layer which name is ln
    """
    layers=QgsProject().instance().mapLayersByName(ln)
    if len(layers)>1:
        print('Warning: there is more than one layer with name',ln)
        return layers[0]
    elif len(layers)==1:
        return layers[0]
    else:
        print('Warning: no matches for', ln)
        return None

# variation over the previous function, to make it more flexible
def my_find_approx_layer(approx_ln):
    """
        tries to find a layer which name includes approx_ln
    """
    layers=QgsProject().instance().mapLayers().values() # dictionairy of all layers
    for layer in layers:
        ln=layer.name()
        if approx_ln in ln: # True if the layer name contains approx_ln
            return my_find_layer(ln)
    return None # in case no match is found


def my_remove_layer(layer):
    """
        removes layer from project
    """
    if layer in QgsProject().instance().mapLayers().values():
        QgsProject().instance().removeMapLayer(layer.id())

def my_create_path_from_list(path_as_list,prefix,suffix,ext="shp"):
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
    """ 
        function to execute processing.run from a list of parameters
        it creates a temporary output (in memory)
        dict_params: dictionary with operation parameters except 'INPUT' and 'OUTPUT'
        layer_name: name for the output layer
        output: output QgsVectorLayer
    """
    dict_params['INPUT']=ln_input
    dict_params['OUTPUT']=QgsProcessing.TEMPORARY_OUTPUT
    mylayer=processing.run(operation,dict_params)['OUTPUT']
    mylayer.setName(layer_name)
    QgsProject().instance().addMapLayer(mylayer)
    return mylayer

def my_export_layer_as_file(mylayer,fn):
    """ 
        function to save QgsVectorLayer as file 
    """
    if isinstance(mylayer,QgsVectorLayer):
        # file name has to be a string
        processing.run("native:savefeatures", {'INPUT':mylayer, 'OUTPUT':str(fn)})

def my_create_project(my_folder,project_name):
    """
        Create new project, set title, and save
    """
    my_project=QgsProject.instance() # QgsProject
    my_project.clear() # Clear project 
    my_project.setTitle(project_name)
    project_file=str(my_folder/project_name)+'.qgz'
    # Save project to file
    my_project.write(project_file) # 

def my_create_project_with_crs(my_folder,project_name,crs_epsg=4326):
    """
        Create new project, set CRS from espg code, set title, and save
    """
    my_project=QgsProject.instance() # QgsProject
    my_project.clear() # Clear project 
    # set project CRS
    my_crs=QgsCoordinateReferenceSystem(crs_epsg)
    my_project.setCrs(my_crs)
    # set project title
    my_project.setTitle(project_name)
    project_file=str(my_folder/project_name)+'.qgz'
    # Save project to file
    my_project.write(project_file) # 
 
def my_add_vector_layer_from_shapefile(fn,ln):
    """
         add and name vector layer from file
         fn: string: path_to_file
         ln: string: output layer name
         output: output layer
    """
    mylayer=QgsVectorLayer(str(fn),"", "ogr")
    # set encoding to utf-8
    provider=mylayer.dataProvider()
    if provider.encoding()!='UTF-8':
        mylayer.dataProvider().setEncoding('UTF-8')
    # set name
    mylayer.setName(ln)
    QgsProject().instance().addMapLayer(mylayer)
    return mylayer

def my_add_layer_from_csv(fn,ln,params):
    """
        reads csv file and adds to project
    """
    # create uri as string
    uri=fn.as_uri()+params
    # create and load layer
    mylayer = QgsVectorLayer(uri, '' , "delimitedtext")
    # encoding
    provider=mylayer.dataProvider()
    if provider.encoding()!='UTF-8':
        mylayer.dataProvider().setEncoding('UTF-8')
    # set name
    mylayer.setName(ln)
    # add to project
    QgsProject().instance().addMapLayer(mylayer)
    return mylayer

def my_add_to_memory_vector_layer_from_shapefile(fn,ln):
    """
         add and name vector layer from file
         fn: string: path_to_file
         ln: string: output layer name
         output: layer copied to memory layer
    """
    mylayer=QgsVectorLayer(str(fn),"", "ogr")
    mylayer.selectAll()
    clone_layer = processing.run("native:saveselectedfeatures", {'INPUT': mylayer, 'OUTPUT': 'memory:'})['OUTPUT']
    mylayer.removeSelection()
    clone_layer.setName(ln)
    QgsProject().instance().addMapLayer(clone_layer)
    return clone_layer

def my_zoom_to_layer(layer_name):
    # Access layer in project if it exists
    mylayers=QgsProject().instance().mapLayersByName(layer_name)
    # mylayer is the first in the returned list
    if mylayers:
        mylayer=mylayers[0]
        # determine CRS
        my_crs=mylayer.crs()
        QgsProject.instance().setCrs(my_crs)
        # Determine extent
        extent = mylayer.extent()
        iface.mapCanvas().setExtent(extent) 
        iface.mapCanvas().refresh()

def my_add_string_attribute_and_compute_value(layer):
    '''
    input: layer
    creates a new field called 'produces' and computes its values from the values of an existing field 'Total'
    '''
    # Create new categorized attribute 'produces' with values 'yes' or 'no'
    fld=QgsField('produces',QVariant.String)
    with edit(layer):
        layer.addAttribute(fld) 
        layer.updateFields()
        for feat in layer.getFeatures():
            if feat['Total'] == 0:
                feat['produces'] = 'no' 
            else:
                feat['produces'] = 'yes' 
            # “update-after-change”
            layer.updateFeature(feat) # 'res' to be silent
            return layer



def my_INE_preprocessing(layer):
    """
        Edits the vector layer and make some changes to it
        The goal is to compute the values of attribute di_co from the values of attribute NUTS_2013
        Only the values of NUTS_2013 with maximum length are of interest (those are the counties)
    """
    # 1st: determine maximum length of NUTS_2013
    maxDigits=0
    for feat in layer.getFeatures():
        if len(feat['NUTS_2013']) > maxDigits:
           maxDigits=len(feat['NUTS_2013'])
    
    # 2nd: for those, compute and store new 4-digit code (last 4 digits) in di_co
    with edit(layer):
        for feat in layer.getFeatures():
            if len(feat['NUTS_2013']) == maxDigits:
                feat['di_co'] = feat['NUTS_2013'][-4:] # last 4 digits
                # “update-after-change”
                res=layer.updateFeature(feat) # 'res' to be silent
    # return output layer
    return layer



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


# adapted from my_create_sturges_graduated_legend_dict(vlayer,attrib,colormap,myopacity,units)  (T19)
def my_create_graduated_legend_from_breaks_dict(breaks,colormap,myopacity,units):
    '''
        This function creates a dictionary to be used as input for setting up the legend
        The classes are defined by the 'breaks' input
        # The inputs for the function are:
        # 1. breaks that define classes
        # 2. the colormap from matplotlib, e.g. 'viridis'
        # 3. a value between 0 and 1 for the opacity of the symbols, e.g. 0.7
        # 4. a string to add information to the classes in the legend, e.g. 'hl' for the units
    '''
    from matplotlib.cm import get_cmap
    import numpy as np
    D={} # initializes dictionary
    count=0
    N=len(breaks)
    # number of classes as the logarithm of the number of observations (Sturges)
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

# updates single band raster layer symbology by stretching to min and max
def my_stretch_single_band_raster_symbology_to_min_max(rlayer):
    '''
        input: single band raster layer
        no output
    '''
    ############################################# reset min and max
    renderer=rlayer.renderer()
    myType = renderer.dataType(1)
    myEnhancement = QgsContrastEnhancement(myType)
    contrast_enhancement = QgsContrastEnhancement.StretchToMinimumMaximum
    myEnhancement.setContrastEnhancementAlgorithm(contrast_enhancement,True)
    # statistics for the raster layer
    stats = provider.bandStatistics(1, QgsRasterBandStats.All, rlayer.extent(), 0)
    # setup min and max
    min = stats.minimumValue
    max = stats.maximumValue
    myEnhancement.setMinimumValue(min)   #Set the minimum value you want
    myEnhancement.setMaximumValue(max)   #Put the maximum value you want 
    # set renderer and refresh
    rlayer.renderer().setContrastEnhancement(myEnhancement)
    rlayer.triggerRepaint()

# This function does not reuire a dictionary of ranges; it mimimcs the QGIS interface
def my_set_vector_graduated_ramp_legend(vlayer,value_field,num_classes,ramp_name):
    '''
        input: vector layer, field with values for symbology, number of classes, color ramp (see below)
        no output
    '''
    # https://gis.stackexchange.com/questions/342352/apply-a-color-ramp-to-vector-layer-using-pyqgis3
    # see possible ramps: print(QgsStyle().defaultStyle().colorRampNames())
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
