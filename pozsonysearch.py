# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:58:59 2019

@author: LokalAdm
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 11:27:17 2019

@author: LokalAdm
"""

from geopy.geocoders import Nominatim
import unicodedata
import codecs
import numpy as np
file = codecs.open("D:/Pozsony.txt", encoding='utf-8')
geolocator = Nominatim(user_agent='talvi')
#location = geolocator.geocode("Czenk (Kis-)")
#print((location.latitude, location.longitude))
vas = []
vasplacenames = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in range(len(l)):
        k = l[i]
        if i:
            lp.append(float(unicodedata.normalize('NFKD', k).encode('ascii','ignore')))
        else:
            i = str(unicodedata.normalize('NFKD', k).encode('ascii','ignore'))
            vasplacenames.append(i[2:(len(i)-1)])
    vas.append(lp)
#print(vasplacenames)
file.close()
vas = np.array(vas)
#tag = vas[0]
#vas = np.transpose(vas[1:])
#print(vas)
#print(tag)
latlong = []
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
        return (listo[k].latitude, listo[k].longitude)
def manual (inpt):
    l = input('We have found no results for ' + inpt + '. Please key in coordinates manually, or key in an alternative search word: ')
    k = l.rstrip().split(' ')
    try:
        float(k[0])
    except ValueError:
        return search(l)
    else:
#    if len(k) == 1:
#        return search(k[0])
#    el
        if len(k) == 2 or len(k) == 4 or len(k) == 6:
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
                return (first, last)
            else:
                return (last, first)
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
        if j1.find('(')!= -1:
            j2 = j1.split('(')
            j1 = j2[-1].replace(')','').replace('-','').rstrip()+j2[0]
        location = geolocator.geocode(j1.rstrip(), exactly_one=False, \
                                      country_codes=['hu','at','si','sk'],\
                                      viewbox = ((45,15),(48.3,18)), bounded=True)
        if location != None:
            locations.extend(location)
        else:
#            if j1.find('(')!= -1:
#                j2 = j1.split('(')
#                j3 = j2[-1].replace(')','').replace('-','').rstrip()+j2[0]
#                location = geolocator.geocode(j3.rstrip(), exactly_one=False, \
#                                      country_codes=['hu','at','si','sk'],\
#                                      viewbox = ((45,15),(48.3,18)), bounded=True)
##                location = geolocator.geocode(j3.rstrip(),False,country=['hu','at','si','sk'])
#                if location != None:
#                    locations.extend(location)
#                else:
#                    if j3.find('cz')!= -1:
#                        location = geolocator.geocode(j3.replace('cz','c').rstrip(), exactly_one=False, \
#                                      country_codes=['hu','at','si','sk'],\
#                                      viewbox = ((45,15),(48.3,18)), bounded=True)
#                        location2 = geolocator.geocode(j3.replace('cz','cs').rstrip(), exactly_one=False, \
#                                      country_codes=['hu','at','si','sk'],\
#                                      viewbox = ((45,15),(48.3,18)), bounded=True)
##                        location = geolocator.geocode(j3.replace('cz','c').rstrip(),False,country=['hu','at','si','sk'])
##                        location2 = geolocator.geocode(j3.replace('cz','cs').rstrip(),False,country=['hu','at','si','sk'])
#                        if location != None:
#                            locations.extend(location)
#                        if location2 != None:
#                            locations.extend(location2)
            if j1.find('cz')!= -1 or j1.find('Cz')!= -1:
                location = geolocator.geocode(j1.replace('cz','c').replace('Cz','C').rstrip(), exactly_one=False, \
                                country_codes=['hu','at','si','sk'],\
                                viewbox = ((45,15),(48.3,18)), bounded=True)
                location2 = geolocator.geocode(j1.replace('cz','cs').replace('Cz','Cs').rstrip(), exactly_one=False, \
                                country_codes=['hu','at','si','sk'],\
                                viewbox = ((45,15),(48.3,18)), bounded=True)
#                location = geolocator.geocode(j1.replace('cz','c').rstrip(),False,country=['hu','at','si','sk'])
#                location2 = geolocator.geocode(j1.replace('cz','cs').rstrip(),False,country=['hu','at','si','sk'])
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
        #if j.latitude < 45 or j.latitude > 48.3 or j.longitude < 15 or \
        #        j.longitude > 18 or (j.raw['countryName']=='Hungary' and j.raw['adminName1']!='Vas'):
        #    valid = False
        accepted_types = ['city', 'borough', 'suburb', 'quarter', 'neighbourhood', 'city_block', 'plot', 'town', 'village', 'hamlet', 'isolated_dwelling', 'allotments', 'trdelnik', 'locality']
        if not ((j.raw['class']== 'place' and j.raw['type'] in accepted_types) or \
                (j.raw['class']== 'boundary' and j.raw['type']=='administrative' )):
            valid = False
            subvalid = True
        if valid:
            for m in validlocs:
                if m == j:
                    valid = False
        if valid:
            validlocs.append(j)
        elif subvalid:
            subvalidlocs.append(j)
    count = len(validlocs)
    if count == 1:
        return (validlocs[0].latitude, validlocs[0].longitude)
    elif count == 0:
        if len(subvalidlocs)!= 0:
            return disambiguation(subvalidlocs, False, inpt)
        else:
            return manual(inpt)
    else:
        return disambiguation(validlocs, True, inpt)#
#ujplacename = []
#ujvas = []
#skipped = []
#for i in range(len(tag)):
#    if i not in skipped:
#        if tag[i]:
#            taggedi = []
#            for j in range(i, len(vas)):
#                if tag[j]== tag[i]:
#                    skipped.append(j)
#                    taggedi.append(j)
#            length = len(vas[i])
#            data = np.zeros(length)
#            placename = ''
#            for j in taggedi:
#                if placename == '':
#                    placename = vasplacenames[j]
#                else:
#                    placename = placename + ", " + vasplacenames[j]
#                for k in range(len(data)):
#                    data[k] += vas[j][k]
#            ujplacename.append(placename)
#            ujvas.append(data)
#        else:
#            ujplacename.append(vasplacenames[i])
#            ujvas.append(vas[i])
#ujvas = np.array(ujvas)

latlong = []
for i in range(len(vasplacenames)):
    latlong.append(search(vasplacenames[i]))
latlong = np.array(latlong)
vas = np.concatenate((latlong, vas), axis = 1)

#uueplacename = []
#uuevas = []
#skipped = []
#for i in range(len(ujplacename)):
#    if i not in skipped:
#        taggedi = []
#        for j in range(i, len(ujplacename)):
#            if ujvas[j][0]== ujvas[i][0]:
#                skipped.append(j)
#                taggedi.append(j)
#        length = len(ujvas[i])
#        data = np.zeros(length)
#        placename = ''
#        data[0] = ujvas[i][0]
#        data[1] = ujvas[i][1]
#        data[2] = ujvas[i][2]
#        for j in taggedi:
#            if placename == '':
#                placename = ujplacename[j]
#            else:
#                placename = placename + ", " + ujplacename[j]
#            for k in range(3, len(data)):
#                data[k] += ujvas[j][k]
#        uueplacename.append(placename)
#        uuevas.append(data)
#ujvas = np.array(ujvas)

#f = open("D:/PozsonyPN.txt","w+")
#for i in vasplacenames:
#    f.write(i)
#    f.write('\n')
#f.close()
#f = open("D:/PozsonyData.txt","w+")
#for lines in vas:
#    f.write('\t'.join([str(j) for j in lines]))
#    f.write('\n')
#f.close()