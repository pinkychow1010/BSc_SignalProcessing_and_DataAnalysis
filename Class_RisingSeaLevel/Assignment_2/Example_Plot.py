# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 10:10:28 2019
@author: Ka Hei Pinky, Chow

Melting Polar Ice: Assignment 2

"""
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import math
import time

from emsc3032.lab2 import read_sph, sph_sum

print ("Standard computations ", time.ctime())

input_file = "GSM-2_2010244-2010273_vl_simple.anpmaly"
print ("Reading the spherical harmonic file: ", input_file)
C,S = read_sph(input_file)

grid_step = 1
lat = np.array(range(-90,181,grid_step))
lon = np.array(range(0,360,grid_step))

results = sph_sum(lat,lon,C,S, process='ewh')

results = results*1e3

