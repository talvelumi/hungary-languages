# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 17:33:56 2019

@author: LokalAdm
"""
import numpy as np
k = np.array([1,2,3])
l = np.array([1.3,5.4,6.8])
print(np.concatenate((k,l)))

def manual (inpt):
    k = input('We have found no results for ' + inpt + '. Please key in coordinates manually, or key in an alternative search word: ')
    k = k.rstrip().split(' ')
    if len(k) == 2:
        return(0, float(k[0]), float(k[1]))
    elif len(k) == 4:
        return(0, int(k[0])+float(k[1])/60, int(k[2])+float(k[3])/60)
    elif len(k) == 6:
        return(0, int(k[0])+(int(k[1])+float(k[2])/60)/60, int(k[3])+(int(k[4])+float(k[5])/60)/60)
    elif len(k) == 1:
        return search(k[0])
    else:
        print('Wrong format')
        return manual(inpt)