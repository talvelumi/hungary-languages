# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 16:22:45 2019

@author: LokalAdm
"""
from geopy.geocoders import GeoNames
import unicodedata
import codecs
import numpy as np

geolocator = GeoNames(username='talvi')
def disambiguation (listo, validity, inpt):
    for i in range(len(listo)):
        print(i)
        print(listo[i])
        print(listo[i].raw)
    if validity: 
        imperfect = ''
    else:
        imperfect = 'imperfect '
    k = int(input('Above are ' + imperfect + 'results we found for ' + inpt + '. Please choose an option or use manual results by -1: '))
    if k == -1:
        return manual(inpt)
    else:
        return (listo[k].raw['geonameId'], listo[k].latitude, listo[k].longitude)
def manual (inpt):
    k = input('We have found no results for ' + inpt + '. Please key in coordinates manually, or key in an alternative search word: ')
    k = k.rstrip().split(' ')
    if len(k) == 1:
        return search(k[0])
    elif len(k) == 2 or len(k) == 4 or len(k) == 6:
        if len(k) == 2:
            first = float(k[0])
            last = float(k[1])
        elif len(k) == 4:
            first = int(k[0])+float(k[1])/60
            last = int(k[2])+float(k[3])/60
        else:
            first = int(k[0])+(int(k[1])+float(k[2])/60)/60
            last = int(k[3])+(int(k[4])+float(k[5])/60)/60
        if first > last:
            return (0, first, last)
        else:
            return (0, last, first)
    else:
        print('Wrong format')
        return manual(inpt)
#for i in vas:
def search (inpt):
    print(inpt)
    k = inpt.split(", ")
    locations = []
    for j in k:
        j1 = j.replace('-','')
        location = geolocator.geocode(j1.rstrip(),False,country=['hu','at','si','sk'])
        if location != None:
            locations.extend(location)
        else:
            if j1.find('(')!= -1:
                j2 = j1.split('(')
                j3 = j2[-1].replace(')','').replace('-','').rstrip()+j2[0]
                location = geolocator.geocode(j3.rstrip(),False,country=['hu','at','si','sk'])
                if location != None:
                    locations.extend(location)
                else:
                    if j3.find('cz')!= -1:
                        location = geolocator.geocode(j3.replace('cz','c').rstrip(),False,country=['hu','at','si','sk'])
                        location2 = geolocator.geocode(j3.replace('cz','cs').rstrip(),False,country=['hu','at','si','sk'])
                        if location != None:
                            locations.extend(location)
                        if location2 != None:
                            locations.extend(location2)
            elif j1.find('cz')!= -1:
                location = geolocator.geocode(j1.replace('cz','c').rstrip(),False,country=['hu','at','si','sk'])
                location2 = geolocator.geocode(j1.replace('cz','cs').rstrip(),False,country=['hu','at','si','sk'])
                if location != None:
                    locations.extend(location)
                if location2 != None:
                    locations.extend(location2)
    validlocs = []
    subvalidlocs = []
    for j1 in range(len(locations)):
        valid = True
        subvalid = False
        j=locations[j1]
        if j.latitude < 45 or j.latitude > 48.3 or j.longitude < 15 or \
                j.longitude > 18 or (j.raw['countryName']=='Hungary' and j.raw['adminName1']!='Vas'):
            valid = False
        elif j.raw['fclName']!= 'city, village,...':
            valid = False
            subvalid = True
        if valid:
            for m in validlocs:
                if m == j:
                    valid = False
        if valid:
            validlocs.append(j)
        elif subvalid:
            subvalidlocs = []
    count = len(validlocs)
    if count == 1:
        return (validlocs[0].raw['geonameId'], validlocs[0].latitude, validlocs[0].longitude)
    elif count == 0:
        if len(subvalidlocs)!= 0:
            return disambiguation(subvalidlocs, False, inpt)
        else:
            return manual(inpt)
    else:
        return disambiguation(validlocs, True, inpt)#

print(search('Nagyczeng'))