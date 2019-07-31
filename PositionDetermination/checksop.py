# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 12:39:21 2019

@author: LokalAdm
"""
import unicodedata
import codecs
import numpy as np
#file = codecs.open("D:/sopron.txt", encoding='utf-8')
#sopron = []
#for line in file:
#    l=line.rstrip().split('\t')
#    lp = []
#    for i in range(len(l)):
#        k = l[i]
#        if i:
#            lp.append(float(unicodedata.normalize('NFKD', k).encode('ascii','ignore')))
#        else:
#            i = str(unicodedata.normalize('NFKD', k).encode('ascii','ignore'))
#            lp.append(i[2:(len(i)-1)])
#    sopron.append(lp)
#
#file = open("D:/sopronll.txt")
#soprony = []
#sopronx = []
#for line in file:
#    l=line.rstrip().split('\t')
#    soprony.append(float(l[0]))
#    sopronx.append(float(l[1]))
#soprony = np.round(np.array(soprony), 3)
#sopronx = np.round(np.array(sopronx), 3)
#for i in range(len(soprony)):
#    for j in range(i):
#        if soprony[i]==soprony[j] and sopronx[i]==sopronx[j]:
#            print(sopron[i][0])
#            print(sopron[j][0])
#            print('\n')

#file = open("D:/moson.txt")
#soprony = []
#sopronx = []
#for line in file:
#    l=line.rstrip().split('\t')
#    soprony.append(float(l[0]))
#    sopronx.append(float(l[1]))
#soprony = np.round(np.array(soprony), 3)
#sopronx = np.round(np.array(sopronx), 3)
#for i in range(len(soprony)):
#    for j in range(i):
#        if soprony[i]==soprony[j] and sopronx[i]==sopronx[j]:
#            print(i)
#            print(j)
#            print('\n')

file = codecs.open("D:/ujvas.txt", encoding='utf-8')
vaspn = []
for line in file:
    l=line.rstrip()
    i = str(unicodedata.normalize('NFKD', l).encode('ascii','ignore'))
    vaspn.append(i[2:(len(i)-1)])

file = open("D:/vasll2.txt")
vasy = []
vasx = []
for line in file:
    l=line.rstrip().split('\t')
    vasy.append(float(l[0]))
    vasx.append(float(l[1]))
vasy = np.round(np.array(vasy), 3)
vasx = np.round(np.array(vasx), 3)
for i in range(len(vasy)):
    for j in range(i):
        if vasy[i]==vasy[j] and vasx[i]==vasx[j]:
            print(vaspn[i])
            print(vaspn[j])
            print('\n')
            print(i,j)