Introductions:
location.py
The Class Ploygon is mainly used to detect if a point is in a ploygon/multiploygon. The method is_in() would return a bool (True/False).
The Class Location is mainly used to detect if a point is in a series of ploygon/multiploygon. The method loc_array() would return a list which could indicate the location of the point.

location_test.py
It is the unit test of the location.py.

./data includes several shapefiles of Los Angeles International Airport (LAX). The shapefiles are sorted by function area: apron, runway, aerodrome.
