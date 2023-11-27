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

