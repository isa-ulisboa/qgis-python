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
        print('Warming: no matches for', ln)
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
    if isinstance(mylayer,QgsVectorLayer):
        mylayer.setName(layer_name)
        QgsProject().instance().addMapLayer(mylayer)
        return mylayer


def my_export_layer_as_file(mylayer,fn):
    """ 
        function to save QgsVectorLayer as file 
    """
    if isinstance(mylayer,QgsVectorLayer):
        # select all features
        mylayer.selectAll()
        # file name has to be a string
        processing.run("native:saveselectedfeatures", {'INPUT':mylayer, 'OUTPUT':str(fn)})
        # unselect
        mylayer.removeSelection()

