# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
file = open("D:/moson.txt")
k = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    k.append(lp)
def color (de, hu, sr, other):
    Total = de+hu+sr+other
    if Total:
        red = de/Total
        green = hu/Total
        blue = sr/Total
        return Total/60, red, green, blue
    else:
        return 0,0,0,0
k = np.transpose(np.array(k))
ky = k[0]
kx = k[1]

def add_bg(w,e,s,n):
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([w, e, s, n], crs=ccrs.PlateCarree())
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
add_bg(16,17.5,47,48.2)
plt.scatter(kx, ky, 4, transform=ccrs.PlateCarree(), zorder=2)
plt.show()

k81= np.transpose(k[2:8])
color81 = []
for i in k81:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]+i[5]
    color81.append(color(de, hu, sr, other))
ky81 = []
kx81 = []
colorplot81 = []
for i in range(len(ky)):
    if color81[i][0]:
        ky81.append(ky[i])
        kx81.append(kx[i])
        colorplot81.append(color81[i])
size = np.transpose(colorplot81)[0]
colorplot81 = np.transpose(np.transpose(colorplot81)[1:])
add_bg(16,17.5,47,48.2)
plt.scatter(kx81, ky81, size, colorplot81, transform=ccrs.PlateCarree(), zorder=2)
plt.show()

k00= np.transpose(k[9:14])
color00 = []
for i in k00:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color00.append(color(de, hu, sr, other))
ky00 = []
kx00 = []
colorplot00 = []
for i in range(len(ky)):
    if color00[i][0]:
        ky00.append(ky[i])
        kx00.append(kx[i])
        colorplot00.append(color00[i])
size = np.transpose(colorplot00)[0]
colorplot00 = np.transpose(np.transpose(colorplot00)[1:])
add_bg(16,17.5,47,48.2)
plt.scatter(kx00, ky00, size, colorplot00, transform=ccrs.PlateCarree(), zorder=2)
plt.show()

k10= np.transpose(k[15:20])
color10 = []
for i in k10:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color10.append(color(de, hu, sr, other))
ky10 = []
kx10 = []
colorplot10 = []
for i in range(len(ky)):
    if color10[i][0]:
        ky10.append(ky[i])
        kx10.append(kx[i])
        colorplot10.append(color10[i])
size = np.transpose(colorplot10)[0]
colorplot10 = np.transpose(np.transpose(colorplot10)[1:])
add_bg(16,17.5,47,48.2)
plt.scatter(kx10, ky10, size, colorplot10, transform=ccrs.PlateCarree(), zorder=2)
plt.show()

k20= np.transpose(k[21:26])
color20 = []
for i in k20:
    de=i[1]
    hu=i[0]
    sr=i[2]
    other =i [3]+i[4]
    color20.append(color(de, hu, sr, other))
ky20 = []
kx20 = []
colorplot20 = []
for i in range(len(ky)):
    if color20[i][0]:
        ky20.append(ky[i])
        kx20.append(kx[i])
        colorplot20.append(color20[i])
size = np.transpose(colorplot20)[0]
colorplot20 = np.transpose(np.transpose(colorplot20)[1:])
add_bg(16,17.5,47,48.2)
plt.scatter(kx20, ky20, size, colorplot20, transform=ccrs.PlateCarree(), zorder=2)
plt.show()