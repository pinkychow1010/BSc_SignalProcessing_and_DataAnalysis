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

print("Fingerprint Values \n")
m = 0
for i in fingerprint:
    print (Location_label[m], i)
    m += 1

#Filling out the table#
#Column 1
print("\nWhen sea level contribution of Greenland, East Antarctica and West Antarctica are\
[_________] respectively, sea level change in the locations are: (round to three effective digits).\n")

#print("\nColumn 1: [0,0,1]m")
"""
def fingerprint(n):
    return (np.array([sph_sum(lat[n],lon[n],C1,S1), sph_sum(lat[n],lon[n],CE,SE), sph_sum(lat[n],lon[n],CW,SW)]))

#print("fingerprint 0",fingerprint(0))
#print(sum(fingerprint(0))
    
fingerprint = []

print (fingerprint(0)*column[0])

column = [[1,0,0], [0,1,0], [0,0,1], [-4,+5,+15], [-0.3,+1.6,+2.5]]
x = 0
for y in column:
    for i in fingerprint():
        print (Location_label[x], round(sum(i*y),3), " m"))
        x += 1
"""

column = [[1,0,0], [0,1,0], [0,0,1], [-4,+5,+15], [-0.3,+1.6,+2.5]]
unit = ["m","m","m","mm","mm"]

u = 0
for k in column:
    x = 0
    print("\n", k, unit[u])
    for i in results:
        print (Location_label[x], round(sum(i*k),3), unit[u])
        x += 1
    u += 1



"""
x = 0
for i in results:
    print (Location_label[x], round(sum(i*[1,0,0]),3), " m")
    x += 1

print("\nColumn 2: [0,1,0]m")
x = 0
for i in results:
    print (Location_label[x], round(sum(i*[0,1,0]),3), " m")
    x += 1

print("\nColumn 3: [0,0,1]m")
x = 0
for i in results:
    print (Location_label[x], round(sum(i*[0,0,1]),3), " m")
    x += 1
    
print("\nColumn 4: [-4,+5,+15]mm")
x = 0
for i in results:
    print (Location_label[x], round(sum(i*[-4,+5,+15]),3), " mm")
    x += 1

print("\nColumn 4: [-0.3,+1.6,+2.5]mm")
x = 0
for i in results:
    print (Location_label[x], round(sum(i*[-0.3,+1.6,+2.5]),3), " mm")
    x += 1
"""    

"""
print("plotting the last two scanerios: ")

input_file = 'Greenland.sph'

#print("\nReading the spherical harmonic file", input_file)
C_g,S_g = read_sph(input_file)

#grid_step = 5
grid_step = 1
lat = np.array(range(-90,90+1,grid_step))
lon = np.array(range(0,360+1,grid_step))

EWH_Greenland = sph_sum(lat,lon,C_g,S_g)

fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection=ccrs.PlateCarree())

mesh = ax.pcolormesh(lon,lat,EWH_Greenland,vmin=-0.2,vmax=1.2,cmap='bwr')
#bwr is only optional
bar = plt.colorbar(mesh,orientation='vertical')

ax.coastlines()
"""

##############################
print("\nQ2: Mitrovica et al (Science, 2001) demonstrated the feasibility of estimating the magnitude of the\
contributions of Greenland, Antarctica and mountain glaciers to eustatic sea level from a global distribution of\
tide gauges.\Assuming that all sea level changes are caused by only Greenland, \
West Antarctica and East Antarctica, use the fingerprint spherical harmonic models of Question 1 \
and the relative sea level changes at the following sites to\
calculate the contributions of each of Greenland, West and East Antarctica.")


print("\nAn inverse of sph_sum need to be done.")








