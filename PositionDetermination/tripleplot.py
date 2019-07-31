# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:25:37 2019

@author: LokalAdm
"""

import matplotlib.pyplot as plt
import numpy as np
import unicodedata
import codecs
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import math

west, east, south, north = 15.7,18.0,46.7,48.4
#west, east, south, north = -179,179,-84,84
def add_bg(w,e,s,n):
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([w, e, s, n], crs=ccrs.PlateCarree())
#    ax.set_extent([-2, 2, -2, 2], crs=ccrs.PlateCarree())
    land = cfeature.NaturalEarthFeature(
        category='physical',
        name='land',
        scale='10m',
        facecolor=np.array([0,0,0]))
    borders = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_boundary_lines_land',
        scale='10m',
        facecolor='none',
        edgecolor='black')
    intbor = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces',
        scale='10m',
        facecolor=cfeature.COLORS['land'])
    rivers = cfeature.NaturalEarthFeature(
        category='physical',
        name='rivers_lake_centerlines',
        scale='10m',
        edgecolor=cfeature.COLORS['water'],
        facecolor='none')
    rivers1 = cfeature.NaturalEarthFeature(
        category='physical',
        name='rivers_europe',
        scale='10m',
        edgecolor=cfeature.COLORS['water'],
        facecolor='none')
    lakes = cfeature.NaturalEarthFeature(
        category='physical',
        name='lakes',
        scale='10m',
        facecolor=cfeature.COLORS['water'])
    lakes1 = cfeature.NaturalEarthFeature(
        category='physical',
        name='lakes_europe',
        scale='10m',
        facecolor=cfeature.COLORS['water'])
    ax.add_feature(land)
    #ax.add_feature(cfeature.OCEAN)
    #ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(intbor)
    ax.add_feature(borders)
    
    #ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(rivers)
    ax.add_feature(rivers1)
    ax.add_feature(lakes)
    ax.add_feature(lakes1)
    return 0
def color (de, hu, sr, other):
    Total = de+hu+sr+other
    if Total:
        red = de/Total
        green = hu/Total
        blue = sr/Total
#        x_color = de / Total
#        y_color = hu/ Total
#        z_color = sr/ Total
#        radius = x_color + y_color + z_color
##        if x_color + y_color + z_color:
##            lat = z_color/(x_color + y_color + z_color) * math.pi/2
##        else:
##            lat = 0
##        if x_color + y_color:
##            long = x_color / (x_color + y_color) * math.pi/2
##        else: 
##            long = 0
##        if radius:
##            subzcolor = z_color/(x_color + y_color + z_color)# * math.pi/2
##            if subzcolor != 1 :
##                lat = math.atan(subzcolor/(1-subzcolor)) 
##            else: 
##                lat = math.pi/2
##        else:
##            lat = 0
##        if x_color + y_color:
##            subxcolor = x_color / (x_color + y_color)
##            if subxcolor != 1 :
##                long = math.atan(subxcolor/(1-subxcolor)) 
##            else: 
##                long = math.pi/2
###        long = x_color / (x_color + y_color) * math.pi/2
##        else: 
##            long = 0
##        red = radius * math.sin(long)* math.cos(lat)
##        green = radius * math.cos(long)* math.cos(lat)
##        blue = radius * math.sin(lat)
#        k = 0.71
#        cyan = np.array([0,1,1])
#        mag = np.array([1,0,1])
#        yellow = np.array([1,1,0])
#        final = k*(cyan * z_color + mag * x_color + yellow * y_color)
#        red = final[0]
#        green = final[1]
#        blue = final[2]
        return Total/50, red, green, blue
    else:
        return 0,0,0,0

file = open("D:/moson.txt")
moson = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    moson.append(lp)

moson = np.transpose(np.array(moson))
mosony = moson[0]
mosonx = moson[1]

file = open("D:/moson90.txt")
moson90 = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    moson90.append(lp)

moson90 = np.array(moson90)


file = codecs.open("D:/sopron.txt", encoding='utf-8')
sopron = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in range(len(l)):
        k = l[i]
        if i:
            lp.append(float(unicodedata.normalize('NFKD', k).encode('ascii','ignore')))
#        else:
#            i = str(unicodedata.normalize('NFKD', k).encode('ascii','ignore'))
#            lp.append(i[2:(len(i)-1)])
    sopron.append(lp)

file = open("D:/sopron90-00.txt")
sopron2 = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    sopron2.append(lp)
    

file = open("D:/sopronll.txt")
soprony = []
sopronx = []
for line in file:
    l=line.rstrip().split('\t')
    soprony.append(float(l[0]))
    sopronx.append(float(l[1]))
#print (soprony)
#print(sopronx)
poplist = []
for i in range(len(soprony)):
    if soprony[i] == 0:
        poplist.append(i)
if len(poplist):
    poplist.reverse()
    for i in poplist:
        soprony.pop(i)
        sopronx.pop(i)
        sopron.pop(i)
        sopron2.pop(i)
#print (soprony)
#print(sopronx)
sopron = np.transpose(np.array(sopron))
sopron2 = np.transpose(np.array(sopron2))

file = open("D:/vasll.txt")
vas = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in range(len(l)):
        k = l[i]
        lp.append(float(k))
#        else:
#            i = str(unicodedata.normalize('NFKD', k).encode('ascii','ignore'))
#            lp.append(i[2:(len(i)-1)])
    vas.append(lp)
    
file = open("D:/vas90.txt")
vas90 = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    vas90.append(lp)



file = open("D:/vasll2.txt")
vasy = []
vasx = []
for line in file:
    l=line.rstrip().split('\t')
    vasy.append(float(l[0]))
    vasx.append(float(l[1]))

poplist2 = []
for i in range(len(vasy)):
    if vasy[i] == 0:
        poplist2.append(i)
if len(poplist2):
    poplist2.reverse()
    for i in poplist2:
        vasy.pop(i)
        vasx.pop(i)
        vas.pop(i)
        vas90.pop(i)
#print (soprony)
#print(sopronx)
vas = np.transpose(np.array(vas))
vas90 = np.array(vas90)

file = open("D:/EastSopronData.txt")
esopron = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    esopron.append(lp)
esopron = np.transpose(np.array(esopron))
esoprony = esopron[0]
esopronx = esopron[1]

file = open("D:/GyorData.txt")
gyor = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    gyor.append(lp)
gyor = np.transpose(np.array(gyor))
gyory = gyor[0]
gyorx = gyor[1]

file = open("D:/PozsonyData.txt")
pozsony = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    pozsony.append(lp)
pozsony = np.transpose(np.array(pozsony))
pozsonyy = pozsony[0]
pozsonyx = pozsony[1]

fullsopronx = np.append (sopronx, esopronx)
fullsoprony = np.append (soprony, esoprony)

add_bg(west, east, south, north)
plt.scatter(mosonx, mosony, 4, transform=ccrs.PlateCarree(), zorder=2, label = 'Moson County')
plt.scatter(fullsopronx, fullsoprony, 4, transform=ccrs.PlateCarree(), zorder=2, label = 'Sopron County')
plt.scatter(vasx, vasy, 4, transform=ccrs.PlateCarree(), zorder=2, label = 'Vas County')
plt.scatter(gyorx, gyory, 4, transform=ccrs.PlateCarree(), zorder=2, label = 'Gyor County')
plt.scatter(pozsonyx, pozsonyy, 4, transform=ccrs.PlateCarree(), zorder=2, label = 'Pozsony County')
#plt.scatter(esopronx, esoprony, 4, transform=ccrs.PlateCarree(), zorder=2, label = 'Eastern Sopron County')
plt.legend()
plt.title('A map of all settlements considered, coloured by county')
plt.show()

totalx = np.array(list(mosonx) + list(sopronx) + list(vasx) + list(esopronx) + list(gyorx) + list(pozsonyx))
totaly = np.array(list(mosony) + list(soprony) + list(vasy) + list(esoprony) + list(gyory) + list(pozsonyy))

moson81= np.transpose(moson[2:8])
sopron81 = np.transpose(sopron[0:6])
vas81 = np.transpose(vas[0:6])
esopron81 = np.transpose(esopron[2:8])
gyor81 = np.transpose(gyor[2:8])
pozsony81 = np.transpose (pozsony[2:8])
##print(sopron81)
color81 = []
for i in moson81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
for i in sopron81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
for i in vas81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
for i in esopron81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
for i in gyor81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
for i in pozsony81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
y81 = []
x81 = []
colorplot81 = []
for i in range(len(totaly)):
    if color81[i][0]:
        y81.append(totaly[i])
        x81.append(totalx[i])
        colorplot81.append(color81[i])
size = np.transpose(colorplot81)[0]
colorplot81 = np.transpose(np.transpose(colorplot81)[1:])
add_bg(west, east, south, north)
plt.scatter(x81, y81, size, colorplot81, transform=ccrs.PlateCarree(), zorder=3)
plt.title('Linguistic situation in 1881')
plt.show()

add_bg(west, east, south, north)
plt.scatter(x81, y81, 5, colorplot81, transform=ccrs.PlateCarree(), zorder=3)
plt.title('Linguistic situation in 1881')
plt.show()

moson10= np.transpose(moson[15:20])
sopron10 = np.transpose(sopron[6:11])
vas10 = np.transpose(vas[11:16])
esopron10 = np.transpose(esopron[18:23])
gyor10 = np.transpose(gyor[18:23])
pozsony10 = np.transpose(pozsony[18:23])
##print(sopron81)
color10 = []
for i in moson10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
for i in sopron10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
for i in vas10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
for i in esopron10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
for i in gyor10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
for i in pozsony10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
y10 = []
x10 = []
colorplot10 = []
for i in range(len(totaly)):
    if color10[i][0]:
        y10.append(totaly[i])
        x10.append(totalx[i])
        colorplot10.append(color10[i])
size = np.transpose(colorplot10)[0]
colorplot10 = np.transpose(np.transpose(colorplot10)[1:])
add_bg(west, east, south, north)
plt.scatter(x10, y10, size, colorplot10, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Linguistic situation in 1910')
plt.show()

add_bg(west, east, south, north)
plt.scatter(x10, y10, 5, colorplot10, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Linguistic situation in 1910')
plt.show()

moson00= np.transpose(moson[9:14])
sopron00 = np.transpose(sopron2[5:10])
vas00 = np.transpose(vas[6:11])
esopron00 = np.transpose(esopron[13:18])
gyor00 = np.transpose(gyor[13:18])
pozsony00 = np.transpose(pozsony[13:18])
##print(sopron81)
color00 = []
for i in moson00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
for i in sopron00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
for i in vas00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
for i in esopron00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
for i in gyor00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
for i in pozsony00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
y00 = []
x00 = []
colorplot00 = []
for i in range(len(totaly)):
    if color00[i][0]:
        y00.append(totaly[i])
        x00.append(totalx[i])
        colorplot00.append(color00[i])
size = np.transpose(colorplot00)[0]
colorplot00 = np.transpose(np.transpose(colorplot00)[1:])
add_bg(west, east, south, north)
plt.scatter(x00, y00, size, colorplot00, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Linguistic situation in 1900')
plt.show()

add_bg(west, east, south, north)
plt.scatter(x00, y00, 5, colorplot00, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Linguistic situation in 1900')
plt.show()

sopron90 = np.transpose(sopron2[0:5])
esopron90 = np.transpose(esopron[8:13])
gyor90 = np.transpose(gyor[8:13])
pozsony90 = np.transpose(pozsony[8:13])
##print(sopron81)
color90 = []
for i in moson90:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color90.append(color(de, hu, sr, other))
for i in sopron90:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color90.append(color(de, hu, sr, other))
for i in vas90:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color90.append(color(de, hu, sr, other))
for i in esopron90:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color90.append(color(de, hu, sr, other))
for i in gyor90:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color90.append(color(de, hu, sr, other))
for i in pozsony90:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color90.append(color(de, hu, sr, other))
y90 = []
x90 = []
colorplot90 = []
for i in range(len(totaly)):
    if color90[i][0]:
        y90.append(totaly[i])
        x90.append(totalx[i])
        colorplot90.append(color90[i])
size = np.transpose(colorplot90)[0]
colorplot90 = np.transpose(np.transpose(colorplot90)[1:])
add_bg(west, east, south, north)
plt.scatter(x90, y90, size, colorplot90, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Linguistic situation in 1891')
plt.show()

add_bg(west, east, south, north)
plt.scatter(x90, y90, 5, colorplot90, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Linguistic situation in 1891')
plt.show()