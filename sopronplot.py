# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 09:27:10 2019

@author: LokalAdm
"""

from geopy.geocoders import GeoNames
import unicodedata
import codecs
file = codecs.open("D:/sopron.txt", encoding='utf-8')
geolocator = GeoNames(username='talvi')
#location = geolocator.geocode("Czenk (Kis-)")
#print((location.latitude, location.longitude))
sopron = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in range(len(l)):
        k = l[i]
        if i:
            lp.append(float(unicodedata.normalize('NFKD', k).encode('ascii','ignore')))
        else:
            i = str(unicodedata.normalize('NFKD', k).encode('ascii','ignore'))
            lp.append(i[2:(len(i)-1)])
    sopron.append(lp)
print(sopron)
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
    k = input('We have found no results for ' + inpt + '. Please key in coordinates manually:')
    k = k.rstrip().split(' ')
    if len(k) == 2:
        return(float(k[0]), float(k[1]))
    elif len(k) == 4:
        return(int(k[0])+float(k[1])/60, int(k[2])+float(k[3])/60)
    elif len(k) == 6:
        return(int(k[0])+(int(k[1])+float(k[2])/60)/60, int(k[3])+(int(k[4])+float(k[5])/60)/60)
    else:
        print('Wrong format')
        return manual(inpt)
for i in sopron:
    print(i)
    k = i[0].split(", ")
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
    validlocs = []
    subvalidlocs = []
    for j1 in range(len(locations)):
        valid = True
        subvalid = False
        j=locations[j1]
        if j.latitude < 45 or j.latitude > 48.3 or j.longitude < 15 or \
                j.longitude > 18 or (j.raw['countryName']=='Hungary' and j.raw['adminName1'][3:]!='r-Moson-Sopron'):
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
        latlong.append((validlocs[0].latitude, validlocs[0].longitude))
    elif count == 0:
        if len(subvalidlocs)!= 0:
            latlong.append(disambiguation(subvalidlocs, False, i[0]))
        else:
            latlong.append(manual(i[0]))
    else:
        latlong.append(disambiguation(validlocs, True, i[0]))
f = open("D:/sopronll.txt","w+")
for lines in latlong:
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