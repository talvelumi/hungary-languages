# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 09:27:10 2019

@author: LokalAdm
"""

from geopy.geocoders import GeoNames
import unicodedata
import codecs
import numpy as np
file = codecs.open("D:/vas.txt", encoding='utf-8')
geolocator = GeoNames(username='talvi')
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
print(vasplacenames)
file.close()
vas = np.transpose(np.array(vas))
tag = vas[0]
vas = np.transpose(vas[1:])
print(vas)
print(tag)
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
ujplacename = []
ujvas = []
skipped = []
for i in range(len(tag)):
    if i not in skipped:
        if tag[i]:
            taggedi = []
            for j in range(i, len(vas)):
                if tag[j]== tag[i]:
                    skipped.append(j)
                    taggedi.append(j)
            length = len(vas[i])
            data = np.zeros(length)
            placename = ''
            for j in taggedi:
                if placename == '':
                    placename = vasplacenames[j]
                else:
                    placename = placename + ", " + vasplacenames[j]
                for k in range(len(data)):
                    data[k] += vas[j][k]
            ujplacename.append(placename)
            ujvas.append(data)
        else:
            ujplacename.append(vasplacenames[i])
            ujvas.append(vas[i])
ujvas = np.array(ujvas)

latlong = []
for i in range(len(ujplacename)):
    latlong.append(search(ujplacename[i]))
latlong = np.array(latlong)
ujvas = np.concatenate((latlong, ujvas), axis = 1)

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

f = open("D:/ujvas.txt","w+")
for i in ujplacename:
    f.write(i)
    f.write('\n')
f.close()
f = open("D:/vasll.txt","w+")
for lines in ujvas:
    f.write('\t'.join([str(j) for j in lines]))
    f.write('\n')
f.close()
#        ll = input("The system cannot find the place. Please input the coordinate from Geonames:")
#        ll = ll.split(' ')
#        lat = int(ll[0])+(int(ll[1])+int(ll[2])/60)/60
#        long = int(ll[3])+(int(ll[4])+int(ll[5])/60)/60
#        latlong.append((lat, long))
#        continue
#    priority = []
#    for j in range(len(locations)):
#        address=str(unicodedata.normalize('NFKD', locations[j].address).encode('ascii','ignore'))
#        address=address[2:(len(address)-1)]
#        k = address.split(', ')
#        print(k)
#        prior = 0
#        if k[1][0] in '123456789':
#            prior += 1000
#        else:
#            for l in k:
#                if l[-5:]==' utca' or l[-3:]==' ut' or l[-4:]==' ter':
#                    prior += 1000
#                    break
#        for j2 in range(j):
#            if locations[j2]==locations[j]:
#                prior += 1000
#                break
#        print(prior)
#        priority.append(prior)
#    count = priority.count(0)