# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:32:40 2019

@author: LokalAdm
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:55:06 2019

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

#class settlement:
#    def __init__ (self, lat, long, de, hu, sr, sk, other, pop1881, pop1891, pop1900, pop1910):
#        self.coord = (lat, long)
#        self.speakers = {'de':de, 'hu':hu, 'sr':sr, 'sk':sk, 'other':other}
#        self.population = {1881:pop1881, 1891:pop1891, 1900:pop1900, 1910:pop1910}
#        for i in range(1882,1891):
#            self.population[i] = (pop1891*(i-1881)+pop1881*(1891-i))/(1891-1881)
#        for i in range(1892,1900):
#            self.population[i] = (pop1900*(i-1891)+pop1891*(1900-i))/(1900-1891)
#        for i in range(1901, 1910): 
#            self.population[i] = (pop1910*(i-1900)+pop1900*(1910-i))/(1910-1900)
#        self.probability = {'de':0, 'hu':0, 'sr':0, 'sk':0, 'other':0}
#
#settlements = []

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
Dinit = np.array([  1, 1,  1,  1,   0.74762004, 0.0001, 0.0001, 0.0001, 0.0001])
settlements = []
speaker0 = []
for line in data:
    settlements.append([line[1],line[0]])
    speaker0.append([line[3], line[2], line[4], line[5], line[6]+line[7]])
settlements = np.array(settlements)
speaker0 = np.array(speaker0)

observed1910 = data[:, 18:23]
observed1910 [:, [0,1]] = observed1910 [:, [1,0]]

observed1900 = data[:, 13:18]
observed1900 [:, [0,1]] = observed1900 [:, [1,0]]

observed1891 = data[:, 8:13]
observed1891 [:, [0,1]] = observed1891 [:, [1,0]]

observed = {1910:observed1910, 1891:observed1891, 1900: observed1900}
pop = {}
pop[1881] = data[:,2:8].sum(axis = 1)
pop[1891] = data[:,8:13].sum(axis = 1)
pop[1900] = data[:,13:18].sum(axis = 1)
pop[1910] = data[:,18:23].sum(axis = 1)

for year in range(1882,1891):
    pop[year]= (1/(1891-1881))*((year-1881)*pop[1891]+(1891-year)*pop[1881])
for year in range(1892,1900):
    pop[year]= (1/(1900-1890))*((year-1891)*pop[1900]+(1900-year)*pop[1891])
for year in range(1901,1910):
    pop[year]= (1/(1910-1900))*((year-1900)*pop[1910]+(1910-year)*pop[1900])

distmat = np.zeros((len(settlements),len(settlements)))
for i in range(len(settlements)):
    for j in range(len(settlements)):
        distmat[i,j] = distance2((settlements[i,0], settlements[i,1]), (settlements[j,0], settlements[j,1]))

def findsse (D):
    constant = {}
    speaker = np.copy(speaker0)
    sse = 0
    rest = D[len(languages):len(D)]
    D = D[0:len(languages)]
    rest = np.append(rest, -rest.sum())
    for year in range(1882,1911):
        for k in range(len(languages)):
            
            d = abs(D[k])
#            for i in range(len(settlements)):
#                for j in range(len(settlements)):
#                    if i-j != 0:
#                        if d==0.:
#                            matrix [i,j] =0
#                        else:
#                            matrix [i,j] = 1/(4*math.pi*d*pop[year-1][i])*math.exp(-1*distmat[i,j]/(4*d))
#    #                    except OverflowError:
#    #                        print (i)
#    #                        print (j)
#    #                        print (k)
#    #                        print (d)
#    #                        matrix [i,j] = 1/(4*math.pi*d)*math.exp(-1*distmat[i,j]/(4*d))
#                    else:
#                        matrix [i,j] = 1
            if d != 0:
                matrix = 1/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
            else:
                matrix = np.zeros((len(settlements),len(settlements)))
            for i in range(len(settlements)):
                matrix[i,i] = math.exp(rest[k]*pop[year-1][i])
            constant[languages[k]] = matrix
        score = []
        for i in range(len(languages)):
            score.append(constant[languages[i]] @ speaker[:,i])
        score = np.transpose(np.array(score))
        totalscore = score.sum(axis=1)
        score = score / totalscore[:,None]
        speaker = score * pop[year][:, None]
        if year in [1891,1900,1910]:
            sse += ((observed[year] - speaker)**2).sum()
    return sse
#print(findsse(Dinit))
res = opt.minimize(findsse, Dinit, method = 'Nelder-Mead', tol = 1)
print(res.x)
print(res.success)
print(res.message)
print(res.fun)
#def gaussian (n, D, distance2):
#    return n/(4*math.pi*D)*math.exp(-1*distance2/(4*D))
#    
#def calculate (settlement, settlements):
#    score = {}
#    for i in languages:
#        score[i] = 0
#        for j in settlements:
#            if distance2(settlement.coord, j.coord):
#                score[i] += gaussian (j.speakers[i], D[i], distance2(settlement.coord, j.coord))
#            else:
#                score[i] += settlement.speakers[i]#/(4*math.pi)
#    totalscore = sum(score.values())
#    for i in languages:
#        settlement.probability[i] = score[i]/totalscore
#    return 0
#
#def update(settlement,year):
#    population = settlement.population[year]
#    for i in languages:
#        settlement.speakers[i] = population * settlement.probability[i]
#    return 0
#for year in range(1882,1911):
#    for i in settlements:
#        calculate(i,settlements)
#    for i in settlements:
#        update(i,year)



#y1 = []
#y2 = []
#for k in arange(12,16,0.1):
#    D = {'de':k, 'hu':k, 'sr':5, 'sk':5, 'other':5}
#    settlements = []
#    a = settlement(47,17, 381,0,0,0,0, 381, 381, 381, 381)
#    b = settlement (47, 17.1, 0, 381, 0, 0, 0, 381, 381, 381, 381)
#    #print (a.coord)
#    #print (a.speakers)
#    #print (a.population)
#    ya = []
#    yb = []
#    yc = []
#    yd = []
#    y = []
#    for i in [a,b]:
#        settlements.append(i)
#    for year in range(1882,1911):
#        for i in settlements:
#            calculate(i, settlements)
#        #print (year)
#        #print (a.probability)
#        #print (b.probability)
#        for i in settlements:
#            update(i, year)
#        #print(a.speakers)
#        #print(b.speakers)
#        ya.append(a.speakers['hu'])
#        #yb.append(b.speakers['hu'])
#        #yc.append(a.speakers['de'])
#        #yd.append(b.speakers['de'])
#    y.append(ya)
#    #y.append(yb)
#    #y.append(yc)
#    #y.append(yd)
#    y1.append(y)
#    y2.append(a.speakers['hu'])
#labels = ['Hungarian speakers in town 1', 'Hungarian speakers in town 2', 'German speakers in town 1', 'German speakers in town 2']
##for i in range(len(y1)):
##    for j in range(len(y1[i])):
##        plt.plot(list(range(1882,1911)), y1[i][j], label= str(i*0.1+0.5))
#plt.plot(list(arange(12,16,0.1)), y2)
##plt.legend()
#plt.show()
    
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

constant = {}
speaker = np.copy(speaker0)
D = res.x
constant = {}
speaker = np.copy(speaker0)
sse = 0
rest = D[len(languages):len(D)]
D = D[0:len(languages)]
rest = np.append(rest, -rest.sum())
for year in range(1882,1911):
    for k in range(len(languages)):
        
        d = abs(D[k])
#            for i in range(len(settlements)):
#                for j in range(len(settlements)):
#                    if i-j != 0:
#                        if d==0.:
#                            matrix [i,j] =0
#                        else:
#                            matrix [i,j] = 1/(4*math.pi*d*pop[year-1][i])*math.exp(-1*distmat[i,j]/(4*d))
#    #                    except OverflowError:
#    #                        print (i)
#    #                        print (j)
#    #                        print (k)
#    #                        print (d)
#    #                        matrix [i,j] = 1/(4*math.pi*d)*math.exp(-1*distmat[i,j]/(4*d))
#                    else:
#                        matrix [i,j] = 1
        if d != 0:
            matrix = 1/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
        else:
            matrix = np.zeros((len(settlements),len(settlements)))
        for i in range(len(settlements)):
            matrix[i,i] = math.exp(rest[k]*pop[year-1][i])
        constant[languages[k]] = matrix
    score = []
    for i in range(len(languages)):
        score.append(constant[languages[i]] @ speaker[:,i])
    score = np.transpose(np.array(score))
    totalscore = score.sum(axis=1)
    score = score / totalscore[:,None]
    speaker = score * pop[year][:, None]
    
comparison = speaker0/pop[1881][:, None]*pop[1910][:, None]
print(np.sum(speaker, axis = 0))
print(np.sum(observed[1910], axis = 0))
print(np.sum(comparison, axis = 0))
print(math.sqrt(((observed[1910] - speaker)**2).sum()/speaker.size))
print(math.sqrt(((observed[1910] - comparison)**2).sum()/speaker.size))
print((abs(observed[1910] - speaker)).sum()/speaker.size)
print((abs(observed[1910] - comparison)).sum()/speaker.size)
color1 = []
for i in range(len(speaker)):
    l = speaker[i]
    other =l[3]+l[4]
    color1.append(color(l[0], l[1], l[2], other))

color1 = np.array(color1)
size = np.transpose(color1)[0]
color1 = np.transpose(np.transpose(color1)[1:])

west, east, south, north = 15.7,18.0,46.7,48.4
add_bg(west, east, south, north)
plt.scatter(settlements[:,1], settlements[:,0], size, color1, transform=ccrs.PlateCarree(), zorder=2)
plt.title('Simulation results')
plt.show()