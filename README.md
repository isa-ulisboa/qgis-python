# qgis-python

QGIS with Python: Open Campus course at ISA/ULisboa

Instructor: Manuel Campagnolo

Start: Monday November 13, 6pm, online (follow zoom link). 10 sessions Mondays and Wednesdays 6-8pm until December 13.

Main links:
* [Zoom link](https://videoconf-colibri.zoom.us/j/98394607195)
* [Fenix: class recordings and evaluation](https://fenix.isa.ulisboa.pt/courses/qwp-846413499991001)
* [Shared folder: data for exercises](https://ulisboa-my.sharepoint.com/:f:/g/personal/mlc_office365_ulisboa_pt/ElM7jQ_b__lEkznQ6mVRuhsBESim1iSIdK0v_7kXgvHw6A?e=gFAj1f) 

## Contents

* [Main resources](#main-resources-for-the-course)
* [QGIS installation](#qgis-instalation)
* [Other useful links](#some-useful-links)

## Main resources for the course 

* Course tutorial and a reference guide: [PyQGIS Developer Cookbook](https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/index.html) or [pdf version](https://docs.qgis.org/testing/pdf/en/QGIS-testing-PyQGISDeveloperCookbook-en.pdf)
  
## QGIS instalation:

*  **Windows**: Follow instructions for [installing QGIS via the OSGeo4W distribution manager](https://www.e-education.psu.edu/geog489/node/2294). You can also follow the video [install QGIS via OSGeo4W](https://www.youtube.com/watch?v=jtHnqvfa6is).
*  **MacOS**: Follow instructions from [Download QGIS](https://www.qgis.org/en/site/forusers/download.html)

Below are included step-by-step instruction for installing QGIS through OSGeo4W (Windows) and using OSGeo4W shell to install Python packages:

1. Downloading and installing QGIS (instructions for installing QGIS via the OSGeo4W distribution manager). [geog489](https://www.e-education.psu.edu/geog489/node/2294)
  - 1st: go to [download](https://qgis.org/en/site/forusers/download.html) and download OSGeo4W Network installer (Window users)
  - 2nd: execute the downloaded file `osgeo4w-setup.exe` (follow instructions in [https://www.e-education.psu.edu/geog489/node/2294](https://www.e-education.psu.edu/geog489/node/2294)): this will take some time. Files will be typically installed in `C:\OSGeo4W`. Note: to uninstall OSGeo4W, run `osgeo4w-setup.exe` and choose advanced installation and choose the packages you want to uninstall (can choose all). Then delete OSGeo4W folder.
  - Important files that are created during installation:
    - `C:\OSGeo4W\OSGeo4W.bat` - This opens the OSGeo4W shell that can be used for executing python scripts from the command line.
    - `C:\OSGeo4W\bin\qgis-ltr-bin.exe` - This is the main QGIS executable that you need to run for starting QGIS 3.
    - Obs: we will execute scripts directly in QGIS, so the OSGeo4W shell (windows key+ OSGeo4W shell) will only be needed to install Python packages (see below).
2. To run the Python interpreter from the OSGeo4W shell one should execute `python-qgis-ltr` (you can exit with `quit()`).
  - [Installing pip](https://pip.pypa.io/en/stable/installation/): most likely not necessary since it should be included in the above installation
  - Installing a Python package that is not included in OSGeo4W: for example, install package `sklearn` (package for Data Science not included in OSGeo4W): 
    - 1st: open OSGeo4W shell (`window key` + `osgeo4w shell`);  
    - 2nd: execute `python -m pip install --user sklearn` in the OSGeo4W shell; 
    - 3rd: in the python console of QGIS do `import sklearn` to verify that it is loaded correctly (i.e. there is no error message)
    - Exercise: install package haversine (distances over the sphere).


## Some useful links

### Documentation (QGIS, PyQGIS):

* (main resource: tutorial and a reference guide) PyQGIS Developer Cookbook. [https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/index.html](https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/index.html) or [https://docs.qgis.org/testing/pdf/en/QGIS-testing-PyQGISDeveloperCookbook-en.pdf](https://docs.qgis.org/testing/pdf/en/QGIS-testing-PyQGISDeveloperCookbook-en.pdf)
* Documentation for QGIS (also accessible through QGIS Python editor). [https://docs.qgis.org/3.28/en/docs/index.html](https://docs.qgis.org/3.28/en/docs/index.html)
* QGIS Python API:  [https://qgis.org/pyqgis/master/core/index.html](https://qgis.org/pyqgis/master/core/index.html)

### Introductory tutorials on PyQGIS
Broad range tutorials:
* PyQGIS 101: Introduction to QGIS Python programming for non-programmers. [https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/](https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/)
* Tutorial on QGIS 3 programming with Python (PyQGIS): [https://www.geodose.com/p/pyqgis.html](https://www.geodose.com/p/pyqgis.html)
* QGIS Tutorials and Tips (with section on PyQGIS): [https://www.qgistutorials.com/en/index.html](https://www.qgistutorials.com/en/index.html)
* Customizing QGIS with Python (Full Course Material) 3.16: [https://courses.spatialthoughts.com/pyqgis-in-a-day.html](https://courses.spatialthoughts.com/pyqgis-in-a-day.html)
* QGIS Python course by Victor Olaya: [https://github.com/volaya/qgis-python-course](https://github.com/volaya/qgis-python-course)
* Automating QGIS3 with Python: [https://www.udemy.com/course/automating-qgis-3xx-with-python/learn/lecture/15679972#overview](https://www.udemy.com/course/automating-qgis-3xx-with-python/learn/lecture/15679972#overview)
* QGIS Python Tutorial (Open source options PyQGIS Tutorial): [https://www.youtube.com/watch?v=X-LvGvNor4E](https://www.youtube.com/watch?v=X-LvGvNor4E)
* Course Unleash QGIS with Python, 2nd edition: [https://github.com/manuelcampagnolo/PyQGIS_2nd_edition](https://github.com/manuelcampagnolo/PyQGIS_2nd_edition)
  
More specific topics:
* PyQGIS: Create and Print a Map Layout with Python: [https://opensourceoptions.com/pyqgis-create-and-print-a-map-layout-with-python/](https://opensourceoptions.com/pyqgis-create-and-print-a-map-layout-with-python/)
* Symbolizing Vector and Raster Layers (2015): [https://www.gislounge.com/symbolizing-vector-and-raster-layers-qgis-python-programming-cookbook/](https://www.gislounge.com/symbolizing-vector-and-raster-layers-qgis-python-programming-cookbook/)
* An Intro to the Earth Engine Python API [https://github.com/google/earthengine-community/blob/master/tutorials/intro-to-python-api/index.ipynb](https://github.com/google/earthengine-community/blob/master/tutorials/intro-to-python-api/index.ipynb)

### Tutorial on creating plugins in QGIS3
* [https://www.qgistutorials.com/en/docs/3/building_a_python_plugin.html](https://www.qgistutorials.com/en/docs/3/building_a_python_plugin.html)
 
### Geopackage and SQLite

* How to create and populate a geopackage in QGIS ([video](https://www.youtube.com/watch?v=rLLP7NImZsU))
* [Load geopackage layers with PyQGIS](https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/pyqgis-101-creating-functions-to-load-geopackage-layers/)
* [How do I do that in SpatialLite and SQLite](https://www.researchgate.net/profile/Arthur-Lembo/publication/313236676_How_do_I_do_that_in_SpatiaLiteSQLite_Illustrating_Classic_GIS_Tasks/links/5893493645851563f828e2de/How-do-I-do-that-in-SpatiaLite-SQLite-Illustrating-Classic-GIS-Tasks.pdf?_sg%5B0%5D=KV_noEuBaQYN_lsdLb8UHcCU0q0Qg1eb6XEsV_zS-EAJdcQ5lGHcDAp07kzuH8bY-ylR1EQmc_JzCwPeMFvO8w.sAO2zeigLecEIg79M9A8H-I8Xqnwkbd1eMEgq8M75MJIbEFy-VC2q_-NnURsSRpRZoxHXhXC8S1oj449J0l5Mw&_sg%5B1%5D=92xoHnfLzUsK1DLwsPzVTrFWy9wjdsZDvdkFL0Kcnur_fQCQSp09YG44puo5ezPLQdMA-M0KWKjbm34fx87kiuvNZ2r1nslGjaPYOxOWTbKJ.sAO2zeigLecEIg79M9A8H-I8Xqnwkbd1eMEgq8M75MJIbEFy-VC2q_-NnURsSRpRZoxHXhXC8S1oj449J0l5Mw&_iepl=) (many examples of spatial SQL queries)

### Geoprocessing with Python (not just with QGIS)
* Geocomputation with Python: [https://py.geocompx.org/](https://py.geocompx.org/). Note: if you have experience on geocomputation with R, check out [https://geocompx.org/](https://geocompx.org/) and the post [https://geocompx.org/post/2023/ogh23/](https://geocompx.org/post/2023/ogh23/) on "Geographic data analysis in R and Python: comparing code and outputs for vector data"
* [PyGIS - Open Source Spatial Programming & Remote Sensing](https://pygis.io/docs/a_intro.html); geowombat; geopandas; rasterio
* There are many available courses on geocomputation with Python, that explore the appropriate Python packages.
 
### Introduction to Python 
* W3schools: [https://www.w3schools.com/python/exercise.asp](https://www.w3schools.com/python/exercise.asp)
* [Python Programming Beginner Tutorials by Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7):

### GDAL
* An Introduction to GDAL: [https://www.youtube.com/watch?v=N_dmiQI1s24](https://www.youtube.com/watch?v=N_dmiQI1s24)

