# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:22:07 2019

@author: Admin
"""

import math
import matplotlib.pyplot as plt
import numpy as np
#import time
#from emsc3032.lab2 import read_sph, sph_sum
#import cartopy.crs as ccrs
#import cartopy.feature as cfeature

def GPS_conversion(x, y, z):
# convert ECEF coordinates to LLA
    a = 6378137
    e = 8.1819190842622e-2

    asq = a**2
    esq = e**2

    b   = math.sqrt(asq * (1 - esq) )
    bsq = b**2

    ep  = math.sqrt((asq - bsq)/bsq)
    p   = math.sqrt(x**2 + y**2)
    th  = math.atan2(a * z, b * p)

    lon = math.atan2(y, x)
    lat = math.atan2( (z + math.pow(ep, 2) * b * math.pow(math.sin(th), 3)),\
                     (p - esq * a * math.pow(math.cos(th), 3)))
    N = a / (math.sqrt(1 - esq * math.pow(math.sin(lat), 2)))
    alt = p / math.cos(lat) - N

    lon = lon * 180 / math.pi
    lat = lat * 180 / math.pi
    return (round(lat, 6), round(lon, 6), round(alt, 6))

data=np.loadtxt('pseudo.obs',skiprows=2)

sat_x=data[:,1]
sat_y=data[:,2]
sat_z=data[:,3]
sat_er=data[:,4]
pseudorange=data[:,5]
sigma=data[:,6]

#CONSTANTS
c = 299792458 #speed of light

n_obs = len(sat_x) 
n_params = 4 #the parameters are (x,y,z) and receiver error

x=1
y=1
z=1
re=1

#Define a pseudorange matrix P
#P = np.zeros((n_obs))
#for i in range(n_obs):
#    P[i] = math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)

A = np.zeros((n_obs,n_params))
b = np.zeros((n_obs))
xhat = np.zeros((n_params))

for iter in range(20):
    for i in range(n_obs): 
        A[i,0] = (x - sat_x[i])/math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)
        A[i,1] = (y - sat_y[i])/math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)
        A[i,2] = (z - sat_z[i])/math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)
        A[i,3] = c
        b[i] = pseudorange[i] - (math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)\
         + c*re - c*sat_er[i]*(10**-6)) #change microsec to sec

    At = np.transpose(A)
    AtA = np.dot(At,A)
    VCV = np.linalg.inv(AtA) 
    Atb = np.dot(At,b)
    xhat = np.dot(VCV,Atb)     
  
    x = x + xhat[0]
    y = y + xhat[1]
    z = z + xhat[2]
    re = re + xhat[3]
            
print("Final parameter estimates:   x= ", round(x,3))
print("Final parameter estimates:   y= ", round(y,3))
print("Final Parameter estimates:   z= ", round(z,3)) 
print("Final Parameter estimates:   receiver error= ", re) 

radius = 6378137 #meters
"""
Exported results:
Latitude,Longitude, Height (ellipsoidal) from ECEF
Latitude  : -69.74246   deg N
Longitude : 73.7112   deg E
Altitude    : 240.4   m

It is locateed in Amery ice shelf, Antarctica.
"""

lat, lon, alt = GPS_conversion(x, y, z)
print("Hence, the GPS coordinates of the location are estimated as:")
print("=================================")
print("Latitude:  ", lat)
print("Longitude:  ", lon)
print("Altitude:  ", alt)
print("=================================")    

#print(VCV)
sigmaX = math.sqrt(VCV.item((0,0)))
sigmaY = math.sqrt(VCV.item((1,1)))
sigmaZ = math.sqrt(VCV.item((2,2)))

sigmaXY = VCV.item((0,1))
sigmaXZ = VCV.item((0,2))
sigmaYZ = VCV.item((2,1))

print("\nUncertainty of x = ", round(math.sqrt(VCV.item((0,0))), 3))
print("Uncertainty of y = ", round(math.sqrt(VCV.item((1,1))), 3))
print("Uncertainty of z = ", round(math.sqrt(VCV.item((2,2))), 3))
print("Uncertainty of clock offset = ", round(math.sqrt(VCV.item((3,3))), 3), "\n")

print("(iv) Calculate the correlations between each parameter")
print("Calculting the correlation between x and y: ")
print(round(sigmaXY*sigmaX*sigmaY, 3))

print("Calculting the correlation between x and z: ")
print(round(sigmaXZ*sigmaX*sigmaZ, 3))

print("Calculting the correlation between y and z: ")
print(round(sigmaYZ*sigmaY*sigmaZ, 3), "\n")

#Weighted least square
W = np.zeros((11, 11))

for i in range(0, 11):
    np.set_printoptions(suppress=True)
    W[i, i] = 1/((sigma[i])**2)

print(W)
#print(np.array_str(W, precision=1, suppress_small=True))

x=1
y=1
z=1
re=1

A = np.zeros((n_obs,n_params))
b = np.zeros((n_obs))
xhat = np.zeros((n_params))

for iter in range(20):
    for i in range(n_obs): 
        A[i,0] = (x - sat_x[i])/math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)
        A[i,1] = (y - sat_y[i])/math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)
        A[i,2] = (z - sat_z[i])/math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)
        A[i,3] = c
        b[i] = pseudorange[i] - (math.sqrt((sat_x[i] - x)**2 + (sat_y[i] - y)**2 + (sat_z[i] - z)**2)\
         + c*re - c*sat_er[i]*(10**-6)) #change microsec to sec

    At = np.transpose(A)
    AtW = np.dot(At,W)
    AtWA = np.dot(AtW,A)
    VCV = np.linalg.inv(AtWA) 
    AtWb = np.dot(AtW,b)
    xhat = np.dot(VCV,AtWb)
  
    x = x + xhat[0]
    y = y + xhat[1]
    z = z + xhat[2]
    re = re + xhat[3]

print("After taking into account the uncertainties of each pseudorange observation:")
print("New parameter estimates:   x= ", round(x,3))
print("New parameter estimates:   y= ", round(y,3))
print("New Parameter estimates:   z= ", round(z,3)) 
print("New Parameter estimates:   receiver error= ", np.around(re, 10)) 
    
lat, lon, alt = GPS_conversion(x, y, z)
print("Hence, the new GPS coordinates of the location are estimated as:")
print("=================================")
print("adjusted_Latitude:  ", lat)
print("adjusted_Longitude:  ", lon)
print("adjusted_Altitude:  ", alt)
print("=================================")    

    
    
    
    
    
    
    
    
    
    
    
    
    
    


