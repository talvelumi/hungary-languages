# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:01:10 2019

@author: LokalAdm
"""

from geopy.geocoders import GeoNames
import json
geolocator = GeoNames(username='talvi')  # Register at Geonames
location = geolocator.geocode("冥府", timeout=10)
if location != None:
#    json.dump(location.raw, f)
    print (location)
else:
    print ("No location!" , location)