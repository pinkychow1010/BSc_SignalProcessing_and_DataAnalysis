# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:33:16 2019
Assignment 2
@author: Ka Chow
"""
#Question 2

import matplotlib.pyplot as plt
import numpy as np
import math
import time
from emsc3032.lab2 import read_sph, sph_sum
import sys
import cartopy.crs as ccrs

print("\nQ2: Mitrovica et al (Science, 2001) demonstrated the feasibility of estimating the magnitude of the\
contributions of Greenland, Antarctica and mountain glaciers to eustatic sea level from a global distribution of\
tide gauges. \nAssuming that all sea level changes are caused by only Greenland, \
West Antarctica and East Antarctica, use the fingerprint spherical harmonic models of Question 1 \
and the relative sea level changes at the following sites to\
calculate the contributions of each of Greenland, West and East Antarctica.\n")

print ("Standard computations ", time.ctime())
input_file_Greenland = "Greenland.sph"
input_file_E_ANT = "E_ANT.sph"
input_file_W_ANT = "W_ANT.sph"

print ("Reading the spherical harmonic files: ", input_file_Greenland, ", ", input_file_E_ANT, ", ", input_file_W_ANT)

C1, S1 = read_sph(input_file_Greenland)
CE, SE = read_sph(input_file_E_ANT)
CW, SW = read_sph(input_file_W_ANT)

lat = [+59.35, +46.51, -10.25, -51.41, -25.38, -49.23, +21.18]
lon = [-149.35, -52.55, +105.41, -57.39, +45.08, +70.11, -157.52]

Location_label = ["Chiswell Island, Alaska", "Capahayden, Canada",  \
                  "Flying Fish Cove, Christmas Island", "Stanley, Faulkland Islands", \
                  "Cap Sainte Marie, Madagascar", "Port aux Francais, Kerguelen", "Honolulu, Hawaii"]

#Fingerprint Value
#results_CI = np.array([sph_sum(lat[0],lon[0],C1,S1), sph_sum(lat[0],lon[0],CE,SE), sph_sum(lat[0],lon[0],CW,SW)])
#results_CC = np.array([sph_sum(lat[1],lon[1],C1,S1), sph_sum(lat[1],lon[1],CE,SE), sph_sum(lat[1],lon[1],CW,SW)])
#results_FFC = np.array([sph_sum(lat[2],lon[2],C1,S1), sph_sum(lat[2],lon[2],CE,SE), sph_sum(lat[2],lon[2],CW,SW)])
#results_St = np.array([sph_sum(lat[3],lon[3],C1,S1), sph_sum(lat[3],lon[3],CE,SE), sph_sum(lat[3],lon[3],CW,SW)])
#results_CSM = np.array([sph_sum(lat[4],lon[4],C1,S1), sph_sum(lat[4],lon[4],CE,SE), sph_sum(lat[4],lon[4],CW,SW)])
#results_Port = np.array([sph_sum(lat[5],lon[5],C1,S1), sph_sum(lat[5],lon[5],CE,SE), sph_sum(lat[5],lon[5],CW,SW)])
#results_Hon = np.array([sph_sum(lat[6],lon[6],C1,S1), sph_sum(lat[6],lon[6],CE,SE), sph_sum(lat[6],lon[6],CW,SW)])

X = np.zeros((7,3))
print("\t Greenland \t\t East Antarctica \t\t West Antarctica")
for i in range(len(lat)):
    X[i,0] = sph_sum(lat[i],lon[i],C1,S1)
    X[i,1] = sph_sum(lat[i],lon[i],CE,SE)
    X[i,2] = sph_sum(lat[i],lon[i],CW,SW)
    print(Location_label[i], "\n", X[i,0], X[i,1], X[i,2])

#results = np.array([results_CI, results_CC, results_FFC, results_St, results_CSM, results_Port, results_Hon])
#fingerprint = [results_CI, results_CC, results_FFC, results_St, results_CSM, results_Port, results_Hon]

#print("\n Fingerprint values: Greenland    E ANT    W ANT    (known) ")
#m = 0
#for i in fingerprint:
 #   print (Location_label[m], i)
  #  m += 1
  
    
#LEAST SQUARE METHOD#

# y = G*Sg + E*Se + W*Sw
sl = [0.52, 0.37, 0.59, 0.50, 0.56, 0.33, 0.63]
y = [Location_label]
n_obs = len(sl) 
n_params = 3 

G=1
E=1
W=1

A = np.zeros((n_obs,n_params))
b = np.zeros((n_obs))
xhat = np.zeros((n_params))

"""
Fingerprint values: Greenland    E ANT    W ANT    (known) 
Chiswell Island, Alaska [0.55135781 1.08139055 1.16325703]
Capahayden, Canada [0.14998769 1.10359553 1.20952197]
Flying Fish Cove, Christmas Island [1.04840974 1.09431411 1.18946191]
Stanley, Faulkland Islands [1.21724306 0.82981494 0.48396257]
Cap Sainte Marie, Madagascar [1.08598872 0.95907216 1.12510645]
Port aux Francais, Kerguelen [1.08896297 0.51595143 0.96216148]
Honolulu, Hawaii [1.09909259 1.17161469 1.23158784]
"""

for iter in range(20):
    for i in range(n_obs): 
        A[i,0] = sph_sum(lat[i],lon[i],C1,S1)
        A[i,1] = sph_sum(lat[i],lon[i],CE,SE)
        A[i,2] = sph_sum(lat[i],lon[i],CW,SW)
        b[i] = sl[i] - (G*A[i,0] + E*A[i,1] + W*A[i,2])

    At = np.transpose(A)
    AtA = np.dot(At,A)
    VCV = np.linalg.inv(AtA) 
    Atb = np.dot(At,b)
    xhat = np.dot(VCV,Atb)     
  
    G = G + xhat[0]
    E = E + xhat[1]
    W = W + xhat[2]        
            
print("Final parameter estimates:   G= ", G)
print("Final parameter estimates:   E= ", E)
print("Final Parameter estimates:   W= ", W) 

    
    
    
    
    
    
    
    
    
    