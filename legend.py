# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 17:09:17 2019

@author: LokalAdm
"""

import math
from matplotlib import pyplot as plt
import ternary
import numpy as np

def color_point(x, y, z, scale):
    w = 255
    x_color = x / float(scale)
    y_color = y/ float(scale)
    z_color = z/ float(scale)
#    radius = x_color + y_color + z_color
#    if radius:
#        subzcolor = z_color/(x_color + y_color + z_color)# * math.pi/2
#        if subzcolor != 1 :
#            lat = math.atan(subzcolor/(1-subzcolor)) 
#        else: 
#            lat = math.pi/2
#    else:
#        lat = 0
#    if x_color + y_color:
#        subxcolor = x_color / (x_color + y_color)
#        if subxcolor != 1 :
#            long = math.atan(subxcolor/(1-subxcolor)) 
#        else: 
#            long = math.pi/2
##        long = x_color / (x_color + y_color) * math.pi/2
#    else: 
#        long = 0
#    g = radius * math.sin(long)* math.cos(lat)
#    r = radius * math.cos(long)* math.cos(lat)
#    b = radius * math.sin(lat)
    cyan = np.array([0,1,1])
    mag = np.array([1,0,1])
    yellow = np.array([1,1,0])
    final = cyan * z_color + mag * x_color + yellow * y_color
    return (final[0], final[1], final[2], 1.)


def generate_heatmap_data(scale=5):
    from ternary.helpers import simplex_iterator
    d = dict()
    for (i, j, k) in simplex_iterator(scale):
        d[(i, j, k)] = color_point(i, j, k, scale)
    return d

fontsize = 10
scale = 100
data = generate_heatmap_data(scale)
figure, tax = ternary.figure(scale=scale)
tax.heatmap(data, style="hexagonal", use_rgba=True, colorbar=False)
tax.boundary()
tax.set_title("Correspondence of color to speaker ratio:", verticalalignment= 'bottom')
tax.clear_matplotlib_ticks()
tax.ticks(axis='lbr', multiple=5, linewidth=1, offset=0.02)
tax.left_axis_label("Serbo-Croatian Speaker Percentage", fontsize=fontsize, offset = 0.12)
tax.right_axis_label("German Speaker Percentage", fontsize=fontsize, offset = 0.12)
tax.bottom_axis_label("Hungarian Speaker Percentage", fontsize=fontsize, offset = 0.1)
tax.get_axes().axis('off')
plt.show()