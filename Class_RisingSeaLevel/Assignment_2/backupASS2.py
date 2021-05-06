# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:33:07 2019

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
#%matplotlib nbagg

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
print("\nWhen sea level of contribution of Greenland, East Antarctica and West Antarctica are 1,0,0m respectively.")
"""
results_Lisbon_col1 = results_Lisbon[0]*1
results_McMurdo_col1 = results_McMurdo[0]*1
results_Hobart_col1 = results_Hobart[0]*1
results_GE_col1 = results_GE[0]*1
results_SanF_col1 = results_SanF[0]*1
results_Kourou_col1 = results_Kourou[0]*1

col1 = [results_Lisbon_col1, results_McMurdo_col1, results_Hobart_col1, results_GE_col1, results_SanF_col1, results_Kourou_col1]
print(col1)
"""
print("\nColumn 1: (round to three effective digits)")
n = 0
for i in results:
    print (Location_label[n], round(sum(i*[1,0,0]),3), " m")
    n += 1

print("\nWhen sea level of contribution of Greenland, East Antarctica and West Antarctica are 0,1,0m respectively.")
print("\nColumn 2:  (round to three effective digits)")
n = 0
for i in results:
    print (Location_label[n], round(sum(i*[0,1,0]),3), " m")
    n += 1
    
print("\nWhen sea level of contribution of Greenland, East Antarctica and West Antarctica are 0,0,1m respectively.")
print("\nColumn 3:  (round to three effective digits)")
n = 0
for i in results:
    print (Location_label[n], round(sum(i*[0,0,1]),3), " m")
    n += 1

    

"""
#Column 2
print("When sea level of contribution of Greenland, East Antarctica and West Antarctica are 0,1,0m respectively.")
results_Lisbon_col2 = results_Lisbon[1]*1
results_McMurdo_col2 = results_McMurdo[1]*1
results_Hobart_col2 = results_Hobart[1]*1
results_GE_col2 = results_GE[1]*1
results_SanF_col2 = results_SanF[1]*1
results_Kourou_col2 = results_Kourou[1]*1
col2 = [results_Lisbon_col2, results_McMurdo_col2, results_Hobart_col2, results_GE_col2, results_SanF_col2, results_Kourou_col2]
print(col2)

#Column 3
print("When sea level of contribution of Greenland, East Antarctica and West Antarctica are 0,0,1m respectively.")
results_Lisbon_col3 = results_Lisbon[2]*1
results_McMurdo_col3 = results_McMurdo[2]*1
results_Hobart_col3 = results_Hobart[2]*1
results_GE_col3 = results_GE[2]*1
results_SanF_col3 = results_SanF[2]*1
results_Kourou_col3 = results_Kourou[2]*1
#Column 4
results_Lisbon_col4 = results_Lisbon_Greenland + results_Lisbon_EANT + results_Lisbon_WANT
results_McMurdo_col4 = results_McMurdo_Greenland + results_McMurdo_EANT + results_McMurdo_WANT
results_Hobart_col4 = results_Hobart_Greenland + results_Hobart_EANT + results_Hobart_WANT
results_GE_col4 = results_GE_Greenland + results_GE_EANT + results_GE_WANT
results_SanF_col4 = results_SanF_Greenland + results_SanF_EANT + results_SanF_WANT
results_Kourou_col4 = results_Kourou_Greenland + results_Kourou_EANT + results_Kourou_WANT
#Column 5
results_Lisbon_col5 = results_Lisbon_Greenland + results_Lisbon_EANT + results_Lisbon_WANT
results_McMurdo_col5 = results_McMurdo_Greenland + results_McMurdo_EANT + results_McMurdo_WANT
results_Hobart_col5 = results_Hobart_Greenland + results_Hobart_EANT + results_Hobart_WANT
results_GE_col5 = results_GE_Greenland + results_GE_EANT + results_GE_WANT
results_SanF_col5 = results_SanF_Greenland + results_SanF_EANT + results_SanF_WANT
results_Kourou_col5 = results_Kourou_Greenland + results_Kourou_EANT + results_Kourou_WANT

print("\nThe sea level rise in the mulitple location is listed as follow:")
print("\nLisbon: ", results_Lisbon)
print("McMurdo: ", results_McMurdo)
print("Hobart: ", results_Hobart)
print("Groote Eylandt, NT, Australia: ", results_GE)
print("San Francisco, USA: ", results_SanF)
print("Kourou, French Guiana: ", results_Kourou)

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


#results_Lisbon_Greenland = sph_sum(lat[0],lon[0],C1,S1)
#results_McMurdo_Greenland = sph_sum(lat[1],lon[1],C1,S1)
#results_Hobart_Greenland = sph_sum(lat[2],lon[2],C1,S1)
#results_GE_Greenland = sph_sum(lat[3],lon[3],C1,S1)
#results_SanF_Greenland = sph_sum(lat[4],lon[4],C1,S1)
#results_Kourou_Greenland = sph_sum(lat[5],lon[5],C1,S1)
#print("Lisbon: ", results_Lisbon, "\nMcMurdo: ", results_McMurdo,\
#      "\nHobart: ", results_Hobart, "\nGroote Eylandt: ",results_GE,\
#      "\nSan Francisco: ", results_SanF, "\nKourou: ", results_Kourou)

#EANT
#print("Fingerprint value for East Antarctica's contribution.")
#results_Lisbon_EANT = sph_sum(lat[0],lon[0],CE,SE)
#results_McMurdo_EANT = sph_sum(lat[1],lon[1],CE,SE)
#results_Hobart_EANT = sph_sum(lat[2],lon[2],CE,SE)
#results_GE_EANT = sph_sum(lat[3],lon[3],CE,SE)
#results_SanF_EANT = sph_sum(lat[4],lon[4],CE,SE)
#results_Kourou_EANT = sph_sum(lat[5],lon[5],CE,SE)
#print("Lisbon: ", results_Lisbon_EANT, "\nMcMurdo: ", results_McMurdo_EANT,\
#      "\nHobart: ", results_Hobart_EANT, "\nGroote Eylandt: ",results_GE_EANT,\
#      "\nSan Francisco: ", results_SanF_EANT, "\nKourou: ", results_Kourou_EANT)

#WANT
#print("Fingerprint value for West Antarctica's contribution.")
#results_Lisbon_WANT = sph_sum(lat[0],lon[0],CW,SW)
#results_McMurdo_WANT = sph_sum(lat[1],lon[1],CW,SW)
#results_Hobart_WANT = sph_sum(lat[2],lon[2],CW,SW)
#results_GE_WANT = sph_sum(lat[3],lon[3],CW,SW)
#results_SanF_WANT = sph_sum(lat[4],lon[4],CW,SW)
#results_Kourou_WANT = sph_sum(lat[5],lon[5],CW,SW)
#print("Lisbon: ", results_Lisbon_WANT, "\nMcMurdo: ", results_McMurdo_WANT,\
#      "\nHobart: ", results_Hobart_WANT, "\nGroote Eylandt: ",results_GE_WANT,\
#      "\nSan Francisco: ", results_SanF_WANT, "\nKourou: ", results_Kourou_WANT)

##############################
print("Q2: Mitrovica et al (Science, 2001) demonstrated the feasibility of estimating the magnitude of the\
contributions of Greenland, Antarctica and mountain glaciers to eustatic sea level from a global distribution of\
tide gauges.\Assuming that all sea level changes are caused by only Greenland, \
West Antarctica and East Antarctica, use the fingerprint spherical harmonic models of Question 1 \
and the relative sea level changes at the following sites to\
calculate the contributions of each of Greenland, West and East Antarctica.")

print("An inverse of sph_sum need to be done.")
"""


