# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 11:20:09 2019

@author: LokalAdm
"""
import numpy as np

file = open("D:/finaldata.txt")
data1 = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    data1.append(lp)
    
data1 = np.array(data1)

file = open("D:/vasll2.txt")
vasll = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    vasll.append(lp)
    
vasll = np.array(vasll)
    
file = open("D:/vas90.txt")
vas90 = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    vas90.append(lp)

vas90 = np.array(vas90)

file = open("D:/vasll.txt")
vas = []
for line in file:
    l=line.rstrip().split('\t')
    lp = []
    for i in l:
        lp.append(float(i))
    vas.append(lp)

vas = np.array(vas)

#vas81 = np.transpose(vas.T[0:6])
vas = np.concatenate((np.transpose(vasll.T[1::-1]), np.transpose(vas.T[0:6]), vas90, np.transpose(vas.T[6:])), axis=1)
data1 = np.concatenate((data1, vas), axis = 0)

f = open("D:/finaldata2.txt","w+")
for lines in data1:
    f.write('\t'.join([str(j) for j in lines]))
    f.write('\n')
f.close()