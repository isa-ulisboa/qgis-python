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
    uri_file=str(fn.as_uri())
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
         add and name vector layer from file and load in memory (so the original layer is not altered)
         fn: string: path_to_file
         ln: string: output layer name
         output: layer copied to memory layer
    """
    mylayer=QgsVectorLayer(str(fn),"", "ogr")
    # copy to memory layer
    mylayer.selectAll()
    params={'INPUT': mylayer, 'OUTPUT': 'memory:'} # to save as memory layer
    clone_layer = processing.run("native:saveselectedfeatures", params)['OUTPUT']
    mylayer.removeSelection()
    print(clone_layer)
    # set encoding to utf-8
    provider=clone_layer.dataProvider()
    if provider.encoding()!='UTF-8':
        clone_layer.dataProvider().setEncoding('UTF-8')
    # set name
    clone_layer.setName(ln)
    QgsProject().instance().addMapLayer(clone_layer)
    return clone_layer

def my_zoom_to_layer(layer_name):
    """
        input: layer name
        works if the project crs is compatible with extent of the input layer
    """
    # Access layer in project if it exists
    mylayers=QgsProject().instance().mapLayersByName(layer_name)
    # mylayer is the first in the returned list
    if mylayers:
        mylayer=mylayers[0]
        # Determine extent
        extent = mylayer.extent()
        iface.mapCanvas().setExtent(extent) 
        iface.mapCanvas().refresh()

