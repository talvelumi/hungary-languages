# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:01:46 2019

@author: LokalAdm
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 14:25:37 2019

@author: LokalAdm
"""

import numpy as np
import unicodedata
import codecs

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


totalx = np.array(list(mosonx) + list(sopronx) + list(esopronx) + list(gyorx) + list(pozsonyx))
totaly = np.array(list(mosony) + list(soprony) + list(esoprony) + list(gyory) + list(pozsonyy))

moson81= np.transpose(moson[2:8])
sopron81 = np.transpose(sopron[0:6])
vas81 = np.transpose(vas[0:6])
esopron81 = np.transpose(esopron[2:8])
gyor81 = np.transpose(gyor[2:8])
pozsony81 = np.transpose (pozsony[2:8])
total81 = np.concatenate((moson81, sopron81, esopron81, gyor81, pozsony81))


moson10= np.transpose(moson[15:20])
sopron10 = np.transpose(sopron[6:11])
vas10 = np.transpose(vas[11:16])
esopron10 = np.transpose(esopron[18:23])
gyor10 = np.transpose(gyor[18:23])
pozsony10 = np.transpose(pozsony[18:23])
total10 = np.concatenate((moson10, sopron10, esopron10, gyor10, pozsony10))




moson00= np.transpose(moson[9:14])
sopron00 = np.transpose(sopron2[5:10])
vas00 = np.transpose(vas[6:11])
esopron00 = np.transpose(esopron[13:18])
gyor00 = np.transpose(gyor[13:18])
pozsony00 = np.transpose(pozsony[13:18])
total00 = np.concatenate((moson00, sopron00, esopron00, gyor00, pozsony00))



sopron90 = np.transpose(sopron2[0:5])
esopron90 = np.transpose(esopron[8:13])
gyor90 = np.transpose(gyor[8:13])
pozsony90 = np.transpose(pozsony[8:13])
total90 = np.concatenate((moson90, sopron90, esopron90, gyor90, pozsony90))

full = np.concatenate((np.reshape(totalx,(len(totalx),1)),np.reshape(totaly,(len(totaly),1)),total81,total90,total00,total10),axis = 1)

equalpairs = []
equallist = []
for i in range(len(full)):
    x = round(full[i][0],3)
    y = round(full[i][1],3)
    for j in range(i):
        x1 = round(full[j][0],3)
        y1 = round(full[j][1],3)
        if x1 == x and y1 == y:
            equalpairs.append(i)
            equalpairs.append(j)
            line = []
            for k in range(len(full[i])):
                if k == 0 or k == 1:
                    line.append(full[i][k])
                else: 
                    if full[i][k] == 0:
                        line.append(full[j][k])
                    elif full[j][k] == 0:
                        line.append(full[i][k])
                    else:
                        #print('Error')
                        line.append(full[j][k]+full[i][k])
            equallist.append(line)
equallist = np.array(equallist)
equalpairs = np.array (equalpairs)

#print(equallist)
#print(equalpairs)
full = np.delete(full, equalpairs, 0)
full = np.concatenate((full, equallist))

transferlist = []
for i in range(len(full)):
    for j in ((2,8),(8,13),(13,18),(18,23)):
        if sum(full[i][j[0]:j[1]]) == 0:
            if i not in transferlist:
                transferlist.append(i)
full = np.delete(full, transferlist, 0)

#for i in range(len(full)):
#    for j in ((2,8),(8,13),(13,18),(18,23)):
#        if sum(full[i][j[0]:j[1]]) == 0:
#            print(i)

f = open("D:/finaldata.txt","w+")
for lines in full:
    f.write('\t'.join([str(j) for j in lines]))
    f.write('\n')
f.close()