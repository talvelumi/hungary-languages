# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:59:08 2019

@author: LokalAdm
"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
def add_bg(w,e,s,n):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
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
add_bg(16,17.5,47,48.5)
plt.show()