# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:22:48 2019

@author: LokalAdm
"""

import math
from vincenty import vincenty
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import scipy.optimize as opt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
def distance2 (ll1,ll2):
    return vincenty(ll1,ll2)**2
viridisBig = cm.get_cmap('brg', 512)
newcmp = ListedColormap(viridisBig(np.linspace(0, 0.5, 256)))

languages = ('de', 'hu', 'sr', 'sk', 'other')

#input data loading process here
file = open("D:/BaranyaTolna2.txt")
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
#Dinit = np.array([ 1, 1, 0.01])
Dinit = np.array([  6.5e-5,6.4e-5,-2.8e-7])
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


observed1910 = np.copy(data[:, 22:27])
observed1910 [:, [0,1]] = observed1910 [:, [1,0]]

observed1900 = np.copy(data[:, 17:22])
observed1900 [:, [0,1]] = observed1900 [:, [1,0]]

observed1891 = np.copy(data[:, 8:17])
observed1891 [:, [0,1]] = observed1891 [:, [1,0]]

observed1920 = np.copy(data[:, 27:32])
observed1920 [:, [0,1]] = observed1920 [:, [1,0]]

observed1930 = np.copy(data[:, 32:38])
observed1930 [:, [0,1]] = observed1930 [:, [1,0]]
observed1930[:, 2] = observed1930[:, 2]+observed1930[:, 4]
observed1930 = np.delete(observed1930, 4, 1)
observed = {1910:observed1910, 1890:observed1891, 1900: observed1900, 1920: observed1920, 1930: observed1930}

observedTest = {}
for year in observed.keys():
    observedTest[year] = observed[year][:, 0:2]
pop = {}
pop[1880] = data[:,2:4].sum(axis = 1)
pop[1890] = data[:,8:10].sum(axis = 1)
pop[1900] = data[:,17:19].sum(axis = 1)
pop[1910] = data[:,22:24].sum(axis = 1)
pop[1920] = data[:,27:29].sum(axis = 1)
pop[1930] = data[:,32:34].sum(axis = 1)

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
    
props = speakerModelling / pop[1880][:, None]
for year in range(1881,1890):
    pop[year]= (1/(1890-1880))*((year-1880)*pop[1890]+(1890-year)*pop[1880])
for year in range(1891,1900):
    pop[year]= (1/(1900-1890))*((year-1890)*pop[1900]+(1900-year)*pop[1890])
for year in range(1901,1910):
    pop[year]= (1/(1910-1900))*((year-1900)*pop[1910]+(1910-year)*pop[1900])
for year in range(1911,1920):
    pop[year]= (1/(1920-1910))*((year-1910)*pop[1920]+(1920-year)*pop[1910])
for year in range(1921,1930):
    pop[year]= (1/(1930-1920))*((year-1920)*pop[1930]+(1930-year)*pop[1920])

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

plotted = speakerModelling[:,0]/speakerModelling.sum(axis = 1)
west, east, south, north = 17.7,19.1,45.7,46.9
#add_bg(west, east, south, north)
#print(plotted)
#plt.scatter(settlements0[:,1], settlements0[:,0], 5, c=plotted, vmin=0, vmax=1, transform=ccrs.PlateCarree(), zorder=2, cmap = newcmp)
#plt.title('Plot of Proportion of German Speakers')
#plt.colorbar()
#plt.show()
distmat = np.zeros((len(settlements0),len(settlements0)))
for i in range(len(settlements0)):
    for j in range(len(settlements0)):
        distmat[i,j] = distance2((settlements0[i,0], settlements0[i,1]), (settlements0[j,0], settlements0[j,1]))
def findsse (D):
    constant = {}
    speaker = np.copy(speakerModelling)
    sse = 0
#    D = (0,0,factk)
    langnum = len(D)-1
    for k in range(langnum):
        
        d = abs(D[k])
        if d != 0:
            matrix = 4/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
        else:
            matrix = np.zeros((len(settlements0),len(settlements0)))
        np.fill_diagonal(matrix, 1)
#        for i in range(len(settlements0)):
#            matrix[i,i]= math.exp(D[-1]*((speaker[i,k]/pop[1880][i])))
        constant[languages[k]] = matrix

    for year in range(1881,1931):
#        for k in range(langnum):
#    
#            d = abs(D[k])
#            if d != 0:
#                matrix = 4/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
#            else:
#                matrix = np.zeros((len(settlements0),len(settlements0)))
##            np.fill_diagonal(matrix, 1)
#            for i in range(len(settlements0)):
#                matrix[i,i]= math.exp((-1)**(k)*((D[-1]*pop[year-1][i])))
#            constant[languages[k]] = matrix
        score = []
        for i in range(langnum):
            score.append(constant[languages[i]] @ speaker[:,i])
        score = np.transpose(np.array(score))
        totalscore = score.sum(axis=1)
        score = score / totalscore[:,None]
        speaker = score * pop[year][:, None]
        if year in [1890,1900,1910, 1920, 1930]:
#            for i in range(len(speaker)):
#                for j in range(len(speaker[i])):
#                    if observedTest[year][i,j]:
#                        sse += ((observedTest[year][i,j] - speaker[i,j])/observedTest[year][i,j])**2
            sse += ((observedTest[year] - speaker)**2).sum()
#    print ('ha')
    return sse
res = opt.minimize(findsse, Dinit, method = 'Nelder-Mead', tol = 0.01)
print(res.x)
#print(res.x)
print(res.success)
print(res.message)
print(res.fun)

constant = {}
D = res.x
#D = Dinit
#D = (0,0,res.x[0])
langnum = len(D)-1
speaker = np.copy(speakerModelling)
for k in range(langnum):
    matrix = np.zeros((len(settlements0),len(settlements0)))
    d = abs(D[k])
    if d != 0:
        matrix = 4/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
    else:
        matrix = np.zeros((len(settlements0),len(settlements0)))
    np.fill_diagonal(matrix, 1)
#    for i in range(len(settlements0)):
#        matrix[i,i]= math.exp(D[-1]*((speaker[i,k]/pop[1880][i])))
    constant[languages[k]] = matrix
totalx, totaly = 0,0
#scoring = {}
#for i in range(langnum):
#    scoring[languages[i]] = np.zeros(len(settlements0))

for year in range(1881,1931):
#    print(year)
    
#    for k in range(langnum):
#        d = abs(D[k])
#        if d != 0:
#            matrix = 4/(4*math.pi*d)*np.exp(-1*distmat/(4*d))
#        else:
#            matrix = np.zeros((len(settlements0),len(settlements0)))
##        np.fill_diagonal(matrix, 1)
#        for i in range(len(settlements0)):
#            matrix[i,i]= math.exp((-1)**(k)*((D[-1]*pop[year-1][i])))
#        constant[languages[k]] = matrix
    score = []
    for i in range(langnum):
#        print(languages[i])
        score.append(constant[languages[i]] @ speaker[:,i])
        for j in range(len(score[i])):
            k = constant[languages[i]][j,j]*speaker[j,i]
            totalx += k
            totaly += score[i][j]-k
#            scoring[languages[i]][j] += score[i][j] - k
#        for j in [0,133,155,196,408,487]:
#            print(j)
#            k=speaker[j,i]*math.exp((-1)**i*D[-1]*pop[year-1][j])
#            print(k)
#            print(score[i][j]-k)
    score = np.transpose(np.array(score))
    totalscore = score.sum(axis=1)
    score = score / totalscore[:,None]
    speaker = score * pop[year][:, None]
print('Habitat term:', totalx)
print('Diffusion term:', totaly)
#for i in scoring.keys():
#    print(i)
#    print(np.sort(scoring[i]))
print(np.sum(speaker, axis = 0))
print(np.sum(observedTest[1930], axis = 0))

comparison = speakerModelling/pop[1880][:, None]*pop[1930][:, None]
print(np.sum(comparison, axis = 0))
print(math.sqrt(((observedTest[1930] - speaker)**2).sum()/speaker.size))
print(math.sqrt(((observedTest[1930] - comparison)**2).sum()/speaker.size))
print((abs(observedTest[1930] - speaker)).sum()/speaker.size)
print((abs(observedTest[1930] - comparison)).sum()/speaker.size)

def fitfunc(k,a,b):
    return a*np.exp(b*k)
smallvillages = []
for i in range(len(speakerModelling)):
    if speakerModelling[i,0] < 100 or pop[1880][i] < 1200:
        smallvillages.append(i)
y = np.delete(speaker[:,0]/pop[1930],smallvillages)/np.delete(speakerModelling[:,0]/pop[1880],smallvillages)
x = np.delete(speakerModelling[:,0]/pop[1880], smallvillages)
plt.plot(x, y, linestyle = '', marker = 'x', mec = '#1f77b4')
#plt.ylim(0,10)
#plt.xlim(0,6000)
#plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x), color = '#419ede')
popt, pcov = opt.curve_fit(fitfunc, x, y)
plt.plot(np.arange(0,1,0.01), fitfunc(np.arange(0,1,0.01), *popt), color = '#419ede', label='y=%5.3f*exp(%5.3fx)' % tuple(popt))
print(1-((y-fitfunc(x, *popt))**2).sum()/((y-np.average(y))**2).sum())
         
smallvillages = []
for i in range(len(speakerModelling)):
    if speakerModelling[i,0] < 100 or pop[1880][i] < 1200:
        smallvillages.append(i)
y = np.delete(observedTest[1930][:,0]/pop[1930],smallvillages)/np.delete(speakerModelling[:,0]/pop[1880],smallvillages)
x = np.delete(speakerModelling[:,0]/pop[1880], smallvillages)
plt.plot(x, y, linestyle = '', marker = 'x', mec = '#ff7f0e')
#plt.ylim(0,10)
#plt.xlim(0,6000)
#plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x), color = '#ffbb0e' )
popt, pcov = opt.curve_fit(fitfunc, x, y)
plt.plot(np.arange(0,1,0.01), fitfunc(np.arange(0,1,0.01), *popt), color = '#ffbb0e', label='y=%5.3f*exp(%5.3fx)' % tuple(popt))
print(1-((y-fitfunc(x, *popt))**2).sum()/((y-np.average(y))**2).sum())
plt.legend()
plt.xlabel('Initial proportion of German speakers')
plt.ylabel('Change in fraction of German speakers')
plt.title('Change in fraction of German language')
plt.show()

smallvillages = []
for i in range(len(speakerModelling)):
    if speakerModelling[i,0] < 100 or pop[1880][i] < 1200:
        smallvillages.append(i)
y = np.delete(speaker[:,0]/pop[1930],smallvillages)/np.delete(speakerModelling[:,0]/pop[1880],smallvillages)
x = np.delete(pop[1880], smallvillages)
plt.plot(x, y, linestyle = '', marker = 'x', mec = '#1f77b4')
#plt.ylim(0,10)
#plt.xlim(0,6000)
plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x), color = '#419ede', label='y=%5.6fx+%5.3f' % tuple(np.polyfit(x, y, 1)))
#popt, pcov = opt.curve_fit(fitfunc, x, y)
#plt.plot(np.arange(0,1,0.01), fitfunc(np.arange(0,1,0.01), *popt), color = '#419ede', label='y=%5.3f*exp(%5.3fx)' % tuple(popt))
print(1-((y-np.poly1d(np.polyfit(x, y, 1))(x))**2).sum()/((y-np.average(y))**2).sum())
         
smallvillages = []
for i in range(len(speakerModelling)):
    if speakerModelling[i,0] < 100 or pop[1880][i] < 1200:
        smallvillages.append(i)
y = np.delete(observedTest[1930][:,0]/pop[1930],smallvillages)/np.delete(speakerModelling[:,0]/pop[1880],smallvillages)
x = np.delete(pop[1880], smallvillages)
plt.plot(x, y, linestyle = '', marker = 'x', mec = '#ff7f0e')
#plt.ylim(0,10)
#plt.xlim(0,6000)
plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x), color = '#ffbb0e', label='y=%5.6fx+%5.3f' % tuple(np.polyfit(x, y, 1)) )
#popt, pcov = opt.curve_fit(fitfunc, x, y)
#plt.plot(np.arange(0,1,0.01), fitfunc(np.arange(0,1,0.01), *popt), color = '#ffbb0e', label='y=%5.3f*exp(%5.3fx)' % tuple(popt))
print(1-((y-np.poly1d(np.polyfit(x, y, 1))(x))**2).sum()/((y-np.average(y))**2).sum())

plt.legend()
plt.xlabel('Initial total population')
plt.ylabel('Change in fraction of German speakers')
plt.title('Change in fraction of German language')
plt.show()

plotted = speaker[:,0]/speaker.sum(axis = 1)
west, east, south, north = 17.7,19.1,45.7,46.9
add_bg(west, east, south, north)
#print(plotted)
plt.scatter(settlements0[:,1], settlements0[:,0], 5, c=plotted, vmin=0, vmax=1, transform=ccrs.PlateCarree(), zorder=2, cmap = newcmp)
plt.title('Plot of Proportion of German Speakers from Simulation')
plt.colorbar()
plt.show()

plotted = speaker[:,0]-speakerModelling[:,0]
west, east, south, north = 17.7,19.1,45.7,46.9
add_bg(west, east, south, north)
#print(plotted)
plt.scatter(settlements0[:,1], settlements0[:,0], 5, c=plotted, vmin=-500, vmax=500, transform=ccrs.PlateCarree(), zorder=2, cmap = newcmp)
plt.title('Plot of Changes in Absolute Number of German Speakers from Simulation')
plt.colorbar()
plt.show()

plotted = speaker[:,0]/pop[1930]-speakerModelling[:,0]/pop[1880]
#print(plotted.shape)
west, east, south, north = 17.7,19.1,45.7,46.9
add_bg(west, east, south, north)
#print(plotted)
plt.scatter(settlements0[:,1], settlements0[:,0], 5, c=plotted, vmin=-max(abs(plotted)), vmax=max(abs(plotted)), transform=ccrs.PlateCarree(), zorder=2, cmap = newcmp)
plt.title('Plot of Changes in Proportion of German Speakers from Simulation')
plt.colorbar()
plt.show()

plotted = (speaker[:,0]-observedTest[1930][:,0])/observedTest[1930].sum(axis = 1)
west, east, south, north = 17.7,19.1,45.7,46.9
add_bg(west, east, south, north)
#print(plotted)
plt.scatter(settlements0[:,1], settlements0[:,0], 5, c=plotted, vmin=-max(abs(plotted)), vmax=max(abs(plotted)), transform=ccrs.PlateCarree(), zorder=2, cmap = newcmp)
plt.title('Plot of relative errors from Simulation')
plt.colorbar()
plt.show()