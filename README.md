# qgis-python
QGIS with Python: Open Campus course at ISA/ULisboa
Instructor: Manuel Campagnolo

## Contents

* [QGIS instalation](#markdown-header-qgis-instalation)
* [Links for the course](#markdown-header-some-useful-links)


## QGIS Instalation:

*  **Windows**: Follow instructions for [installing QGIS via the OSGeo4W distribution manager ](https://www.e-education.psu.edu/geog489/node/2294). After installation, you can verify the path with `sys.executable` which should return something like `C:\\OSGeo4W\\bin\\qgis-ltr-bin.exe`. You can also follow the video [install QGIS via OSGeo4W](https://www.youtube.com/watch?v=jtHnqvfa6is).
*  **MacOS**: Follow instructions from [Download QGIS](https://www.qgis.org/en/site/forusers/download.html)

Below are included step-bystep instruction for installing QGIS through OSGeo4W (windows) and using OSGeo4W shell to install Python packages:

1. Downloading and installing QGIS (instructions for installing QGIS via the OSGeo4W distribution manager). [https://www.e-education.psu.edu/geog489/node/2294]
  - 1st: go to [https://qgis.org/en/site/forusers/download.html] and download OSGeo4W Network installer (Window users)
  - 2nd: execute the downloaded file `osgeo4w-setup.exe` (follow instructions in [https://www.e-education.psu.edu/geog489/node/2294]): this will take some time. Files will be typically installed in `C:\OSGeo4W`. Note: to uninstall OSGeo4W, run `osgeo4w-setup.exe` and choose advanced installation and choose the packages you want to uninstall (can choose all). Then delete OSGeo4W folder.
  - Important files that are created during installation:
    - C:\OSGeo4W\OSGeo4W.bat - This opens the OSGeo4W shell that can be used for executing python scripts from the command line.
    - C:\OSGeo4W\bin\qgis-ltr-bin.exe - This is the main QGIS executable that you need to run for starting QGIS 3.
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

* (main resource: tutorial and a reference guide) PyQGIS Developer Cookbook. [https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/index.html] or [https://docs.qgis.org/testing/pdf/en/QGIS-testing-PyQGISDeveloperCookbook-en.pdf]
* Documentation for QGIS (also accessible through QGIS Python editor). [https://docs.qgis.org/3.22/en/docs/index.html]
* QGIS Python API:  [https://qgis.org/pyqgis/master/core/index.html]

### Introductory tutorials on PyQGIS:

* PyQGIS 101: Introduction to QGIS Python programming for non-programmers. [https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/]
* Tutorial on QGIS 3 programming with Python (PyQGIS). [https://www.geodose.com/p/pyqgis.html]
* QGIS Tutorials and Tips (with section on PyQGIS)
* Customizing QGIS with Python (Full Course Material) 3.16: [https://courses.spatialthoughts.com/pyqgis-in-a-day.html]
* QGIS in macOS:
  - QGIS macOS packages: [https://www.kyngchaos.com/software/qgis/]
  - discussion on Installing Python modules for QGIS 3 on MacOS: see instructions to set path in QGIS to the directory with python modules

### Tutorial on creating plugins in QGIS3: 
* [https://www.qgistutorials.com/en/docs/3/building_a_python_plugin.html]

### Python simple interactive exercises: 
* [https://www.w3schools.com/python/exercise.asp]

### Python code examples: Hot Examples (Search Python code examples from over 1.000.000 projects). 
* [https://python.hotexamples.com]

### Geoprocessing with Python (not just in QGIS): 
* [PyGIS - Open Source Spatial Programming & Remote Sensing](https://pygis.io/docs/a_intro.html); geowombat; geopandas; rasterio

### Geopackage and SQLite:

* How to create and populate a geopackage in QGIS ([video](https://www.youtube.com/watch?v=rLLP7NImZsU))
* [Load geopackage layers with PyQGIS](https://anitagraser.com/pyqgis-101-introduction-to-qgis-python-programming-for-non-programmers/pyqgis-101-creating-functions-to-load-geopackage-layers/)
* [Working with Geospatial Data: An Introduction](https://www.fulcrumapp.com/blog/working-with-geodata) (SQLite and geopackage in QGIS; no PyQGIS)
* [How do I do that in SpatialLite and SQLite](https://www.researchgate.net/profile/Arthur-Lembo/publication/313236676_How_do_I_do_that_in_SpatiaLiteSQLite_Illustrating_Classic_GIS_Tasks/links/5893493645851563f828e2de/How-do-I-do-that-in-SpatiaLite-SQLite-Illustrating-Classic-GIS-Tasks.pdf?_sg%5B0%5D=KV_noEuBaQYN_lsdLb8UHcCU0q0Qg1eb6XEsV_zS-EAJdcQ5lGHcDAp07kzuH8bY-ylR1EQmc_JzCwPeMFvO8w.sAO2zeigLecEIg79M9A8H-I8Xqnwkbd1eMEgq8M75MJIbEFy-VC2q_-NnURsSRpRZoxHXhXC8S1oj449J0l5Mw&_sg%5B1%5D=92xoHnfLzUsK1DLwsPzVTrFWy9wjdsZDvdkFL0Kcnur_fQCQSp09YG44puo5ezPLQdMA-M0KWKjbm34fx87kiuvNZ2r1nslGjaPYOxOWTbKJ.sAO2zeigLecEIg79M9A8H-I8Xqnwkbd1eMEgq8M75MJIbEFy-VC2q_-NnURsSRpRZoxHXhXC8S1oj449J0l5Mw&_iepl=) (many examples of spatial SQL queries)

### Layer legends:

* Categorized legend for vector layer: [https://gis.stackexchange.com/questions/318474/setting-style-for-categorized-vector-in-pyqgis]

### [Python Programming Beginner Tutorials by Corey Schafer](https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7):

* Lists, Tuples, and Sets
* Strings - Working with Textual Data
* Dictionaries
* Loops and iterations
* Python comprehensions are a very natural and easy way to create lists, dicts, and sets
* Functions
* How to read and write to file
* How to work with csv files using the csv module
* Modules, import, sys.path, random, math, os, webbrowser
* os Module
* How to read, write, and match regular expressions with the re module
* Working with JSON Data using the json Module
* Datetime Module - How to work with Dates, Times, Timedeltas, and Timezones
* Classes and Instances
* About inheritance and how to create subclasses
* Class Variables
* Classmethods and staticmethods
* iterators and iterables
* Pandas using Python.
* Pandas DataFrame and Series objects.
* Pandas indexes.
* How to get started with Matplotlib.
* Create bar charts in Matplotlib.
* Create pie charts in Matplotlib.
* Create histograms in Matplotlib.
* Create scatter plots in Matplotlib.

### GDAL: 
* An Introduction to GDAL: [https://www.youtube.com/watch?v=N_dmiQI1s24]

