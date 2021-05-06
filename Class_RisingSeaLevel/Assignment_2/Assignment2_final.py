Assign# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 12:56:10 2019
@author: Ka Hei Pinky, Chow

Q1. Mitrovica et al. (2001) showed how the global footprint of mass loss of glaciated regions could
be combined with measurements of sea level from tide gauges to learn about the mass changes.
For the values of eustatic sea level (or ESL rate) given, calculate the changes in sea level \
at the following locations.

"""
import matplotlib.pyplot as plt
import numpy as np
import math
import time
from emsc3032.lab2 import read_sph, sph_sum
import sys
import cartopy.crs as ccrs

print("Q1. For the values of eustatic sea level (or ESL rate) given, calculate the changes in sea level \
      at the following locations")

print ("Standard computations ", time.ctime())
input_file_Greenland = "Greenland.sph"
input_file_E_ANT = "E_ANT.sph"
input_file_W_ANT = "W_ANT.sph"

print ("Reading the spherical harmonic files: ", input_file_Greenland, ", ", input_file_E_ANT, ", ", input_file_W_ANT)

C1, S1 = read_sph(input_file_Greenland)
CE, SE = read_sph(input_file_E_ANT)
CW, SW = read_sph(input_file_W_ANT)


#Setting up latitude and lontitude for the given locations
lat = [38.722252, -75.25772, -42.8819, -12.379 ,37.774929, 5.161131]
lon = [-9.139337,	97.81815,	147.32381	, 130.886993, -122.419418, -52.649334]

Location_label = ["Lisbon, Portugal", "McMurdo, Antarctica", "Hobart, TAS, Australia", \
                  "Groote Eylandt, NT, Australia", "San Francisco, CA, USA", "Kourou, French Guiana"]

#Fingerprint Value

print("\n (a). Fingerprint\nFingerprint values for contribution of Greenland, East Antarctica and West Antarctica are: ")

results_Lisbon = np.array([sph_sum(lat[0],lon[0],C1,S1), sph_sum(lat[0],lon[0],CE,SE), sph_sum(lat[0],lon[0],CW,SW)])
results_McMurdo = np.array([sph_sum(lat[1],lon[1],C1,S1), sph_sum(lat[1],lon[1],CE,SE), sph_sum(lat[1],lon[1],CW,SW)])
results_Hobart = np.array([sph_sum(lat[2],lon[2],C1,S1), sph_sum(lat[2],lon[2],CE,SE), sph_sum(lat[2],lon[2],CW,SW)])
results_GE = np.array([sph_sum(lat[3],lon[3],C1,S1), sph_sum(lat[3],lon[3],CE,SE), sph_sum(lat[3],lon[3],CW,SW)])
results_SanF = np.array([sph_sum(lat[4],lon[4],C1,S1), sph_sum(lat[4],lon[4],CE,SE), sph_sum(lat[4],lon[4],CW,SW)])
results_Kourou = np.array([sph_sum(lat[5],lon[5],C1,S1), sph_sum(lat[5],lon[5],CE,SE), sph_sum(lat[5],lon[5],CW,SW)])
results = np.array([results_Lisbon, results_McMurdo, results_Hobart, results_GE, results_SanF, results_Kourou])
fingerprint = [results_Lisbon, results_McMurdo, results_Hobart, results_GE, results_SanF, results_Kourou]

print("\n (a). Fingerprint\nFingerprint values for contribution of Greenland, East Antarctica and West Antarctica are: ")
m = 0
for i in fingerprint:
    print (Location_label[m], i)
    m += 1


print("\n (b). Sea level change\nWhen sea level contribution of Greenland, East Antarctica and West Antarctica are\
[_________] respectively, sea level change in the locations are: (round to three effective digits).\n")

column = [[1,0,0], [0,1,0], [0,0,1], [-4,+5,+15], [-0.3,+1.6,+2.5]]
unit = ["m","m","m","mm","mm"]

#Showing every column in the table
u = 0
for k in column:
    x = 0
    print("\n", k, unit[u])
    for i in results:
        print (Location_label[x], round(sum(i*k),3), unit[u])
        x += 1
    u += 1
    


M = np.zeros((6,5))

print("\t\t\t Greenland \t\t East Antarctica \t\t West Antarctica")
for i in range(len(lat)): #location 
    for m in range(len(column)):
        M[i,m] = round(sph_sum(lat[i],lon[i],C1,S1)*column[m][0] + \
         sph_sum(lat[i],lon[i],CE,SE)*column[m][1] + sph_sum(lat[i],lon[i],CW,SW)*column[m][2], 3)
    print(M[i])
        
        
        
        #print(Location_label[m], "\n", M[i,0], M[i,1], M[i,2])

"""
V1 = [round(sum(results[0]*column[0]),3), round(sum(results[0]*column[1]),3), \
     round(sum(results[0]*column[2]),3), round(sum(results[0]*column[3]),3), \
     round(sum(results[0]*column[4]),3)]
V2 = [round(sum(results[1]*column[0]),3), round(sum(results[1]*column[1]),3), \
     round(sum(results[1]*column[2]),3), round(sum(results[1]*column[3]),3), \
     round(sum(results[1]*column[4]),3)]
V3 = [round(sum(results[2]*column[0]),3), round(sum(results[2]*column[1]),3), \
     round(sum(results[2]*column[2]),3), round(sum(results[2]*column[3]),3), \
     round(sum(results[2]*column[4]),3)]
V4 = [round(sum(results[3]*column[0]),3), round(sum(results[3]*column[1]),3), \
     round(sum(results[3]*column[2]),3), round(sum(results[3]*column[3]),3), \
     round(sum(results[3]*column[4]),3)]
V5 = [round(sum(results[4]*column[0]),3), round(sum(results[4]*column[1]),3), \
     round(sum(results[4]*column[2]),3), round(sum(results[4]*column[3]),3), \
     round(sum(results[4]*column[4]),3)]
V6 = [round(sum(results[5]*column[0]),3), round(sum(results[5]*column[1]),3), \
     round(sum(results[5]*column[2]),3), round(sum(results[5]*column[3]),3), \
     round(sum(results[5]*column[4]),3)]

    
print( '\t\t', "Greenland / E Ant / W Ant")
print("Location", '\t\t', column)
print("--------------------------------------------------------------------------------------")
print(Location_label[0], '\t', V1)
print(Location_label[1], '\t', V2)
print(Location_label[2], '\t', V3)
print(Location_label[3], '\t', V4)
print(Location_label[4], '\t', V5)
print(Location_label[5], '\t', V6)
"""
######Checking Fingerprint Values#####

grid_step = 1
lat_plot = np.array(range(-90,90+1,grid_step))
lon_plot = np.array(range(0,360+1,grid_step))

EWH_Greenland = sph_sum(lat_plot,lon_plot,C1,S1)
EWH_EANT = sph_sum(lat_plot,lon_plot,CE,SE)
EWH_WANT = sph_sum(lat_plot,lon_plot,CW,SW)

fig1 = plt.figure(figsize=(10,5))
ax1 = plt.axes(projection=ccrs.PlateCarree())

plt.title('Greenland Fingerprint Values')
meshc1 = ax1.pcolormesh(lon_plot,lat_plot,EWH_Greenland,vmin=-0.5,vmax=+1.5,cmap='hsv')
bar = plt.colorbar(meshc1,orientation='vertical')

ax1.coastlines()

fig2 = plt.figure(figsize=(10,5))
ax2 = plt.axes(projection=ccrs.PlateCarree())

plt.title('East Antarctica Fingerprint Values')
meshc2 = ax2.pcolormesh(lon_plot,lat_plot,EWH_EANT,vmin=-0.5,vmax=1.5,cmap='hsv')
bar = plt.colorbar(meshc2,orientation='vertical')

ax2.coastlines()

fig2 = plt.figure(figsize=(10,5))
ax2 = plt.axes(projection=ccrs.PlateCarree())

plt.title('Wast Antarctica Fingerprint Values')
meshc3 = ax2.pcolormesh(lon_plot,lat_plot,EWH_WANT,vmin=-0.5,vmax=1.5,cmap='hsv')
bar = plt.colorbar(meshc3,orientation='vertical')

ax2.coastlines()


######Plotting the map###########
print("\nPlotting the last two scanerios: ")

grid_step = 5
#grid_step = 1
lat_plot = np.array(range(-90,90+1,grid_step))
lon_plot = np.array(range(0,360+1,grid_step))

EWH_Greenland = sph_sum(lat_plot,lon_plot,C1,S1)
EWH_EANT = sph_sum(lat_plot,lon_plot,CE,SE)
EWH_WANT = sph_sum(lat_plot,lon_plot,CW,SW)

#first plot
print("When sea level contribution of Greenland, East Antarctica and West Antarctica are -4,+5,+15 mm.")
EWH_SUM_S1 = EWH_Greenland*-4 + EWH_EANT*5 + EWH_WANT*15
fig1 = plt.figure(figsize=(10,5))
ax1 = plt.axes(projection=ccrs.PlateCarree())

plt.title('Mapping the sea level change in the first scanerio')
mesh1 = ax1.pcolormesh(lon_plot,lat_plot,EWH_SUM_S1,vmin=-30,vmax=+30,cmap='hsv')
bar = plt.colorbar(mesh1,orientation='vertical')

ax1.coastlines()

#second plot
print("When sea level contribution of Greenland, East Antarctica and West Antarctica are -0.3,+1.6,+2.5 mm.")
EWH_SUM_S2 = EWH_Greenland*-0.3 + EWH_EANT*1.6 + EWH_WANT*2.5
fig2 = plt.figure(figsize=(10,5))
ax2 = plt.axes(projection=ccrs.PlateCarree())

plt.title('Mapping the sea level change in the second scanerio')
mesh2 = ax2.pcolormesh(lon_plot,lat_plot,EWH_SUM_S2,vmin=-30,vmax=30,cmap='hsv')
bar = plt.colorbar(mesh2,orientation='vertical')

ax2.coastlines()

print("the End of Question 1")
