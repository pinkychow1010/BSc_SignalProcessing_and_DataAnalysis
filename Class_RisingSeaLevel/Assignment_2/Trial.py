# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:55:04 2019

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:06:34 2019

Q1. Mitrovica et al. (2001) showed how the global footprint of mass loss of glaciated regions could
be combined with measurements of sea level from tide gauges to learn about the mass changes.
The spatial “fingerprint” of (dimensionless) mass loss of East Antarctica, West Antarctica and Greenland,
expressed in terms of spherical harmonic coefficients, can be found on the Wattle site in folder “Assignment 2”

i) E_Antarctic.sph
ii) W_Antarctic.sph
iii) Greenland.sph
"""
import matplotlib.pyplot as plt
import numpy as np
import math
import time
from emsc3032.lab2 import read_sph, sph_sum
import sys
import cartopy.crs as ccrs

print("For the values of eustatic sea level (or ESL rate) given, calculate the changes in sea level \
      at the following locations")

print ("Standard computations ", time.ctime())
input_file_Greenland = "Greenland.sph"
input_file_E_ANT = "E_ANT.sph"
input_file_W_ANT = "W_ANT.sph"

print ("Reading the spherical harmonic files: ", input_file_Greenland, ", ", input_file_E_ANT, ", ", input_file_W_ANT)

C1, S1 = read_sph(input_file_Greenland)
CE, SE = read_sph(input_file_E_ANT)
CW, SW = read_sph(input_file_W_ANT)

grid_step = 1
lat = np.array(range(-90,181,grid_step))
lon = np.array(range(0,360,grid_step))
lat = [38.722252, -75.25772, -42.8819, -12.379 ,37.774929, 5.161131]
lon = [-9.139337,	97.81815,	147.32381	, 130.886993, -122.419418, -52.649334]

Lisbon = [lat[0],lon[0]]
McMurdo = [lat[1],lon[1]]
Hobart = [lat[2],lon[2]]
GE = [lat[3],lon[3]]
SanF = [lat[4],lon[4]]
Kourou = [lat[5],lon[5]]

Location_label = ["Lisbon, Portugal", "McMurdo, Antarctica", "Hobart, TAS, Australia", \
                  "Groote Eylandt, NT, Australia", "San Francisco, CA, USA", "Kourou, French Guiana"]

#Fingerprint Value
print("\nFingerprint values for contribution of Greenland, East Antarctica and West Antarctica are respectively: ")
results_Lisbon = np.array([sph_sum(lat[0],lon[0],C1,S1), sph_sum(lat[0],lon[0],CE,SE), sph_sum(lat[0],lon[0],CW,SW)])
results_McMurdo = np.array([sph_sum(lat[1],lon[1],C1,S1), sph_sum(lat[1],lon[1],CE,SE), sph_sum(lat[1],lon[1],CW,SW)])
results_Hobart = np.array([sph_sum(lat[2],lon[2],C1,S1), sph_sum(lat[2],lon[2],CE,SE), sph_sum(lat[2],lon[2],CW,SW)])
results_GE = np.array([sph_sum(lat[3],lon[3],C1,S1), sph_sum(lat[3],lon[3],CE,SE), sph_sum(lat[3],lon[3],CW,SW)])
results_SanF = np.array([sph_sum(lat[4],lon[4],C1,S1), sph_sum(lat[4],lon[4],CE,SE), sph_sum(lat[4],lon[4],CW,SW)])
results_Kourou = np.array([sph_sum(lat[5],lon[5],C1,S1), sph_sum(lat[5],lon[5],CE,SE), sph_sum(lat[5],lon[5],CW,SW)])
results = np.array([results_Lisbon, results_McMurdo, results_Hobart, results_GE, results_SanF, results_Kourou])
fingerprint = [results_Lisbon, results_McMurdo, results_Hobart, results_GE, results_SanF, results_Kourou]
m = 0
for i in fingerprint:
    print (Location_label[m], i)
    m += 1

#Filling out the table#
#Column 1
print("\nWhen sea level contribution of Greenland, East Antarctica and West Antarctica are\
[_________] respectively, sea level change in the locations are: (round to three effective digits).")

print("\nColumn 1: [0,0,1]m")

def fingerprint(n):
    return (np.array([sph_sum(lat[n],lon[n],C1,S1), sph_sum(lat[n],lon[n],CE,SE), sph_sum(lat[n],lon[n],CW,SW)]))


print("fingerprint 0",fingerprint(0))
print(np.sum(fingerprint(0))