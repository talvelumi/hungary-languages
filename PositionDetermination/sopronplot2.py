# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:05:17 2019

@author: LokalAdm
"""

import matplotlib.pyplot as plt
import numpy as np
import unicodedata
import codecs
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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

file = open("D:/moson.txt")
moson = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    moson.append(lp)
def color (de, hu, sr, other):
    Total = de+hu+sr+other
    if Total:
        red = de/Total
        green = hu/Total
        blue = sr/Total
        return Total/50, red, green, blue
    else:
        return 0,0,0,0
moson = np.transpose(np.array(moson))
mosony = moson[0]
mosonx = moson[1]


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
for i in poplist:
    soprony.pop(i)
    sopronx.pop(i)
    sopron.pop(i)
#print (soprony)
#print(sopronx)
sopron = np.transpose(np.array(sopron))
add_bg(16,17.5,47,48.2)
plt.scatter(mosonx, mosony, 4, transform=ccrs.PlateCarree(), zorder=2)
plt.scatter(sopronx, soprony, 4, transform=ccrs.PlateCarree(), zorder=2)
plt.show()

totalx = np.array(list(mosonx) + list(sopronx))
totaly = np.array(list(mosony) + list(soprony))

moson81= np.transpose(moson[2:8])
sopron81 = np.transpose(sopron[0:6])
#print(sopron81)
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
add_bg(16,17.5,47,48.2)
plt.scatter(x81, y81, size, colorplot81, transform=ccrs.PlateCarree(), zorder=2)
plt.show()

moson10= np.transpose(moson[15:20])
sopron10 = np.transpose(sopron[6:11])
#print(sopron81)
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
add_bg(16,17.5,47,48.2)
plt.scatter(x10, y10, size, colorplot10, transform=ccrs.PlateCarree(), zorder=2)
plt.show()