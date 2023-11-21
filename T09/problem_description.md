QGIS with Python: Open Campus course at ISA/ULisboa

November-December 2023

Instructor: Manuel Campagnolo

## T09: Milk production (INE)

### Data sets:
1.	Shapefile: CAOP: official map of Portuguese continental counties
2.	CSV: Milk production, INE

The code of the feature in CAOP is a string with up to 7 characters. The counties correspond to the features with 7 characters exactely. The other feature are higher level administrative units that are not of interest for the problem. The county 4-digit code corresponds to the last of those 7 digits. That county code matches the county code in the INE file.

### Goals:
1.	Make a map of Portugal that represents the milk production per county.
2.	Choose the type of milk for the map (goat, cow, or sheep)
3.	Define a meaningful legend for the map
