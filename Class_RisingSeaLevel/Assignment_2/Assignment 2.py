# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Created on Thu Mar 21 10:57:57 2019

@author: Admin
"""
"""
Q1 (10 marks) Mitrovica et al. (2001) showed how the global footprint of mass loss of glaciated regions could
be combined with measurements of sea level from tide gauges to learn about the mass changes.
The spatial “fingerprint” of (dimensionless) mass loss of East Antarctica, West Antarctica and Greenland,
expressed in terms of spherical harmonic coefficients, can be found on the Wattle site in folder “Assignment 2”

i) E_Antarctic.sph
ii) W_Antarctic.sph
iii) Greenland.sph
"""

import matplotlib.pyplot as plt
import numpy as np
#from mpl_toolkits.basemap import Basemap
import math
import time
from emsc3032.lab2 import read_sph, sph_sum
from time import sleep
import sys

#Cmn and Smn
#from the data of greenand....sph

#Pmn
#from emse3032.lab1 import lpmn
#lpmn(math.cos(alt),max_degree)
#max_degree = 256
"""
lat = [38.722252, -75.25772, -42.8819, -12.379 ,37.774929, 5.161131]
lon = [-9.139337,	97.81815,	147.32381	, 130.886993, -122.419418, -52.649334]

Lisbon = [lat[0],lon[0]]
McMurdo = [lat[1],lon[1]]
Hobart = [lat[2],lon[2]]
GE = [lat[3],lon[3]]
SanF = [lat[4],lon[4]]
Kourou = [lat[5],lon[5]]
"""
Lisbon_lat = 38.722252
Lisbon_lon = -9.139337
"""
Lisbon_TF = Lisbon_EA + Lisbon_WN + Lisbon_GL
McMurdo_TF = McMurdo_EA + McMurdo_WN + McMurdo_GL
Hobart_TF = Hobart_EA + Hobart_WN + Hobart_GL
GE_TF = GE_EA + GE_WN + GE_GL
SanF_TF = SanF_EA + SanF_WN + SanF_GL
McMurdo_TF = McMurdo_EA + McMurdo_WN + McMurdo_GL
"""

print ("Standard computations ", time.ctime())

data_greenland=np.loadtxt('Greenland.sph',skiprows=1)
print ("Reading the spherical harmonic file: ", data_greenland)

n_col=data_greenland[:,0]
m_col=data_greenland[:,1]
C_col=data_greenland[:,2]
S_col=data_greenland[:,3]

n_obs = len(m_col) 

print ("Standard computations ", time.ctime())

data_greenland=np.loadtxt('Greenland.sph',skiprows=1)
input_file = "Greenland.sph"
print ("Reading the spherical harmonic file: ", data_greenland)
C, S = read_sph(data_greenland)

grid_step = 1
lat = np.array(range(-90,181,grid_step))
lon = np.array(range(0,360,grid_step))

results = sph_sum(Lisbon_lat,Lisbon_lon,C,S, process='ewh')

results = results*1e3

print(results)






"""
print("Longtitude of Lisbon:", Lisbon[1])
t = 0
part = 0
for n in range (len(n_col)):
     for m in range (len(m_col)):
         #if (m == t):
         part += C_col[n]*math.cos(m*Lisbon[1]) + S_col[n]*math.sin(m*Lisbon[1])
             #print("n,m,C ",n,m,C_col[n])
         t += 1
         sys.stdout.flush()
         sleep(1)           

print("Sum of (C cos + S sin): ", part)
"""
         


























"""
#import sys
#! conda install --yes --prefix {sys.prefix} cartopy

#! {sys.executable} - mpip install -u -i https

#from emsc3032.lab2 import read_sph, sph_sum

print ("Standard computations ", time.ctime())

data_greenland=np.loadtxt('Greenland.sph',skiprows=1)
#input_file = "GSM-2_2010244-2010273_vl_simple.anpmaly"
print ("Reading the spherical harmonic file: ", data_greenland)
C,S = read_sph(data_greenland)

grid_step = 1
#lat = np.array(range(-90,181,grid_step))
#lon = np.array(range(0,360,grid_step))

lat_Lisbon = 38.722252
lon_Lisbon = -9.139337


results = sph_sum(lat_Lisbon,lon_Lisbon,C,S, process='ewh')

results = results*1e3

print("Generating the global map", time.ctime())
plt.figure()

#X1,Y1 = np.meshgrid(lon,lat)
#m = Basemap(projection='kav7', lon_0=10, resolution='1')

"""





























