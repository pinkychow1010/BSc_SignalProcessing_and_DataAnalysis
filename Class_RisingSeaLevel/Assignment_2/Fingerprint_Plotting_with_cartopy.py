# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 21:56:18 2019

@author: Admin
"""

from emsc3032.lab2 import read_sph, sph_sum
import sys
import cartopy.crs as ccrs #have to download first!

import numpy as np
#%matplotlib nbagg
import matplotlib.pyplot as plt

input_file = 'Greenland.sph'
print("Reading the spherical harmonic file", input_file)
C_g,S_g = read_sph(input_file)

grid_step = 5
#grid_step = 1
lat = np.array(range(-90,90+1,grid_step))
lon = np.array(range(0,360+1,grid_step))

EWH_Greenland = sph_sum(lat,lon,C_g,S_g)

fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection=cors.PlateCarree())

mesh = ax.pcolormesh(lon,lat,EWH_Greenland,vmin=-0.2,vmax=1.2,cmap='bwr')
#bwr is only optional
bar = plt.colorbar(mesh,orientation='vertical')

ax.coastlines()





