# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 11:39:37 2019

@author: LokalAdm
"""

# =============================================================================
# import numpy as np
# cyan = np.array([0,1,1])
# mag = np.array([1,0,1])
# yellow = np.array([1,1,0])
# print(cyan/3+mag/3+yellow/3)
# =============================================================================

from vincenty import vincenty
import math
import numpy
#print(vincenty ((-90,90), (90,90)))
pop =numpy.array( [1,2])
dist =numpy.array([ [1,2],[3,4]])
print(numpy.exp(dist)/pop[:,None])
#a = numpy.array([2,-3,-4])
#print(abs(a))