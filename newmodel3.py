# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:24:32 2019

@author: LokalAdm
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:29:17 2019

@author: LokalAdm
"""

import math
from vincenty import vincenty
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import scipy.optimize as opt
def distance2 (ll1,ll2):
    return vincenty(ll1,ll2)**2

languages = ('de', 'hu', 'sr', 'sk', 'other')

#input data loading process here
file = open("D:/finaldata.txt")
data = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    data.append(lp)
#for line in data:
#    settlements.append(settlement(line[1],line[0], line[3], line[2], line[4], line[5], line[6]+line[7], sum(line[2:8]), sum(line[8:13]), sum(line[13:18]), sum(line[18:23])))
data = np.array(data)
#D = {'de':14, 'hu':14, 'sr':14, 'sk':14, 'other':14} #Testing purpose, do not trust
#Dinit = np.array([  2.8796892,  106.4799405,   10.09502287,   0.61053932,   0.84524969])#3.06733121
#Dinit = np.array([  3.06733109, 121.91322502,   5.24350383,  16.59367886,   0.79454929])
#Dinit = np.array([ 4.24138189e+04,  6.90749573e-01,  1.48903524e+05,  1.68392701e+02,       -2.38063878e+02])
Dinit = np.array([  2.08466626, 129.48974141, 0.00001])
#Dinit = np.array([  6,6,6,6,6,6])
#Dinit = np.array([-1.91255781e-08,  1.93718199e+01,  -1.91255781e-08, -1.91255781e-08,
#  -1.91255781e-08,  2.77199829e-01])
settlements = []
speaker0 = []
for line in data:
    settlements.append([line[1],line[0]])
    speaker0.append([line[3], line[2], line[4], line[5], line[6]+line[7]])
settlements = np.array(settlements)
speaker0 = np.array(speaker0)
speakerModelling = speaker0[:, 0:2]
emptyplaces = []
for i in range(len(speakerModelling.sum(axis = 1))):
    if speakerModelling.sum(axis = 1)[i]==0:
        emptyplaces.append(i)


observed1910 = data[:, 18:23]
observed1910 [:, [0,1]] = observed1910 [:, [1,0]]

observed1900 = data[:, 13:18]
observed1900 [:, [0,1]] = observed1900 [:, [1,0]]

observed1891 = data[:, 8:13]
observed1891 [:, [0,1]] = observed1891 [:, [1,0]]

observed = {1910:observed1910, 1891:observed1891, 1900: observed1900}

observedTest = {}
for year in observed.keys():
    observedTest[year] = observed[year][:, 0:2]
pop = {}
pop[1881] = data[:,2:4].sum(axis = 1)
pop[1891] = data[:,8:10].sum(axis = 1)
pop[1900] = data[:,13:15].sum(axis = 1)
pop[1910] = data[:,18:20].sum(axis = 1)

for year in observed.keys():
#    print(year)
    for i in range(len(speakerModelling.sum(axis = 1))):
        if (observed[year][:, 0:2].sum(axis = 1))[i]==0:
            if i not in emptyplaces:
                emptyplaces.append(i)

speakerModelling = np.delete(speakerModelling, emptyplaces, 0)
settlements0 = np.delete(settlements, emptyplaces, 0)
for i in observedTest.keys():
    observedTest[i]= np.delete(observedTest[i], emptyplaces, 0)
for i in pop.keys():
    pop[i]= np.delete(pop[i], emptyplaces, 0)

percentage = speakerModelling / pop[1881][:,None]    

for year in range(1882,1891):
    pop[year]= (1/(1891-1881))*((year-1881)*pop[1891]+(1891-year)*pop[1881])
for year in range(1892,1900):
    pop[year]= (1/(1900-1890))*((year-1891)*pop[1900]+(1900-year)*pop[1891])
for year in range(1901,1910):
    pop[year]= (1/(1910-1900))*((year-1900)*pop[1910]+(1910-year)*pop[1900])
    
distmat = np.zeros((len(settlements0),len(settlements0)))
for i in range(len(settlements0)):
    for j in range(len(settlements0)):
        distmat[i,j] = distance2((settlements0[i,0], settlements0[i,1]), (settlements0[j,0], settlements0[j,1]))
def findsse (D):
    constant = {}
    speaker = np.copy(speakerModelling)
    sse = 0
    langnum = len(D)-1
    for k in range(langnum):
            
        d = abs(D[k])
        if d != 0:
            matrix = 1/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
        else:
            matrix = np.zeros((len(settlements0),len(settlements0)))
#        np.fill_diagonal(matrix, 1)
        for i in range(len(settlements0)):
            matrix[i,i]= math.exp((-1)**k*D[-1]*percentage[i,k])
        constant[languages[k]] = matrix

    for year in range(1882,1911):
#        for k in range(langnum):
#                
#            d = abs(D[k])
#            if d != 0:
#                matrix = 1/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
#            else:
#                matrix = np.zeros((len(settlements0),len(settlements0)))
#            np.fill_diagonal(matrix, 1)
#            for i in range(len(settlements0)):
#                matrix[i,i]= math.exp((-1)**k*D[-1]*pop[year-1][i])
#            constant[languages[k]] = matrix
        score = []
        for i in range(langnum):
            score.append(constant[languages[i]] @ speaker[:,i])
        score = np.transpose(np.array(score))
        totalscore = score.sum(axis=1)
        score = score / totalscore[:,None]
        speaker = score * pop[year][:, None]
        if year in [1891,1900,1910]:
#            for i in range(len(speaker)):
#                for j in range(len(speaker[i])):
#                    if observedTest[year][i,j]:
#                        sse += ((observedTest[year][i,j] - speaker[i,j])/observedTest[year][i,j])**2
            sse += ((observedTest[year] - speaker)**2).sum()
    return sse
res = opt.minimize(findsse, Dinit, method = 'Nelder-Mead', tol = 0.01)
print(res.x)
print(res.x)
print(res.success)
print(res.message)
print(res.fun)

constant = {}
D = res.x
langnum = len(D)-1
for k in range(langnum):
    matrix = np.zeros((len(settlements0),len(settlements0)))
    d = abs(D[k])
    if d != 0:
        matrix = 1/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
    else:
        matrix = np.zeros((len(settlements0),len(settlements0)))
#    np.fill_diagonal(matrix, 1)
    for i in range(len(settlements0)):
        matrix[i,i]= math.exp((-1)**k*D[-1]*percentage[i,k])
    constant[languages[k]] = matrix

speaker = np.copy(speakerModelling)
for year in range(1882,1911):
#    for k in range(langnum):
#            
#        d = abs(D[k])
#        if d != 0:
#            matrix = 1/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
#        else:
#            matrix = np.zeros((len(settlements0),len(settlements0)))
#            np.fill_diagonal(matrix, 1)
#        for i in range(len(settlements0)):
#            matrix[i,i]= math.exp((-1)**k*D[-1]*pop[year-1][i])
#        constant[languages[k]] = matrix
    score = []
    for i in range(langnum):
        score.append(constant[languages[i]] @ speaker[:,i])
    score = np.transpose(np.array(score))
    totalscore = score.sum(axis=1)
    score = score / totalscore[:,None]
    speaker = score * pop[year][:, None]
print(np.sum(speaker, axis = 0))
print(np.sum(observedTest[1910], axis = 0))

comparison = speakerModelling/pop[1881][:, None]*pop[1910][:, None]
print(np.sum(comparison, axis = 0))
print(math.sqrt(((observedTest[1910] - speaker)**2).sum()/speaker.size))
print(math.sqrt(((observedTest[1910] - comparison)**2).sum()/speaker.size))
print((abs(observedTest[1910] - speaker)).sum()/speaker.size)
print((abs(observedTest[1910] - comparison)).sum()/speaker.size)
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

speakerplot = np.insert(speaker, emptyplaces, 0, axis = 0)
color1 = []
for i in range(len(speakerplot)):
    l = speakerplot[i]
    k = observed[1910][i]
    other = k[3]+k[4]
    color1.append(color(l[0], l[1], k[2], other))

color1 = np.array(color1)
size = np.transpose(color1)[0]
color1 = np.transpose(np.transpose(color1)[1:])

west, east, south, north = 15.7,18.0,46.7,48.4
add_bg(west, east, south, north)
plt.scatter(settlements[:,1], settlements[:,0], size, color1, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Simulation results')
plt.show()

plotted = (speaker[:,0]-observedTest[1910][:,0])/observedTest[1910].sum(axis = 1)
west, east, south, north = 15.7,18.0,46.7,48.4
add_bg(west, east, south, north)
#print(plotted)
plt.scatter(settlements0[:,1], settlements0[:,0], 5, c=plotted, vmin=-max(abs(plotted)), vmax=max(abs(plotted)), transform=ccrs.PlateCarree(), zorder=2)
plt.title('Plot of errors')
plt.colorbar()
plt.show()