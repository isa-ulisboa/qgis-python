# Code needs to be adapted for the correct paths
processing.run("native:extractbylocation", 
{'INPUT':'C:\\Users\\PyQGIS\\Documents\\sessions\\s1_stopvespa\\input\\Cont_Conc_CAOP2022.shp',
'PREDICATE':[0],
'INTERSECT':'delimitedtext://file:///C:/Users/PyQGIS/Documents/sessions/s1_stopvespa/input/STOPVespa_2023_simplified.csv?type=csv&delimiter=;&maxFields=10000&detectTypes=yes&xField=long&yField=lat&crs=EPSG:4326&spatialIndex=yes&subsetIndex=no&watchFile=no',
'OUTPUT':'C:/Users/PyQGIS/Documents/sessions/s1_stopvespa/output/Conc_stop_vespa_3.shp'})
