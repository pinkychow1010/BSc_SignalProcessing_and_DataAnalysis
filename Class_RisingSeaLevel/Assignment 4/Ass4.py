# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:56:56 2019

@author: Ka Hei
"""

#import packages needed for the analysis and plotting
import cartopy.crs as ccrs
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import cartopy.feature as cfeature

#Define function to normalize data for plotting
class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):

        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
    
norm = MidpointNormalize(midpoint=0)

#Setting up a customized colour bar for use in (iii)
cmap = plt.cm.jet_r 
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(-0.25, 0.25, 20)
norm_customized = mpl.colors.BoundaryNorm(bounds, cmap.N)


#(i) derive and plot the unregularised solution for the gravity field anomalies for this 15-day period
#import data from the file
data_AtWA=np.loadtxt('AtWA.data', skiprows = 2)
data_AtWB=np.loadtxt('AtWB.data')
data_msc=np.loadtxt('mascons.latlon')

with open('mascons.regions', 'r') as f:
    x = f.readlines()
regions=[]
for s in range(len(x)):
    regions += [x[s].strip(' ').strip('\n').split(' ')]
    
#print(regions)
    #Land/Ocean/Grnld/Antar
    
VCV = np.linalg.inv(data_AtWA)
AtWb = data_AtWB[:,1]
AtWb.shape

#print(AtWb[:-336,:-336])

xhat = np.dot(VCV,AtWb)
xhat_red = xhat [:-336]

lat = data_msc [:,1]
lon = data_msc [:,2]

fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())
#mesh = ax.scatter(lon,lat,c=xhat_red, s=30, cmap= "seismic_r", vmin=-500, vmax=500)
mesh = ax.scatter(lon,lat,c=xhat_red, s=30, norm = norm, cmap= "seismic_r")

plt.title('Unregularized MASCON solution', fontsize=16)
bar = plt.colorbar(mesh, orientation='vertical')

ax.coastlines()

#(ii) derive and plot your best global estimate of the mass changes 
#a. using Tikhonov regularisation

#Assign same value for every region
C = np.identity(7863)
for i in range(7527):
    C[:,i] *= 8000

AtWA = data_AtWA 
VCV = np.linalg.inv(AtWA + C) 
AtWb = data_AtWB[:,1]

xhat = np.dot(VCV,AtWb)
xhat_red = xhat [:-336]

lat = data_msc [:,1]
lon = data_msc [:,2]

fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

#mesh = ax.scatter(lon,lat,c=xhat_red, s=30, norm = norm, cmap='seismic_r', vmin=-1, vmax=1)
mesh = ax.scatter(lon,lat,c=xhat_red, s=30, norm = norm, cmap='seismic_r')
bar = plt.colorbar(mesh, orientation='vertical')
plt.title('Tikhonov regularization of MASCON solution', fontsize=16)

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

#ii b. using region-specific regularisation. What values did you assign to each region?

C = np.identity(7863)
sigma = 1
n = 14
# Assigning values for regularization
for i in range(1, len(regions)-1):
    s = n/(sigma**2)
    i = int(i)
    if regions[i][1] == 'Ocean':
        if regions[i+1][1] == 'Alask' or regions[i+1][1] == 'Antar' or regions[i+1][1] == 'Grnld':
            sigma = 0.1
            C[:,i] *= s
        elif regions[i-1][1] == 'Alask' or regions[i-1][1] == 'Antar' or regions[i-1][1] == 'Grnld':
            sigma = 0.1
            C[:,i] *= s
        elif xhat_red[i]*xhat_red[i+1]<0 or  xhat_red[i]*xhat_red[i-1]<0:
            sigma = 0.01
            C[:,i] *= s
        else:
            sigma = 0.015
            C[:,i] *= s          
    elif regions[i][1] == 'Land':
        sigma = 0.04
        C[:,i] *= s
#        if xhat_red[i]*xhat_red[i+1]<0 or xhat_red[i]*xhat_red[i-1]<0:
#            sigma = 0.05
#            C[:,i] *= s
#        else:
#            sigma = 0.1
#            C[:,i] *= s
    elif regions[i][1] == 'Grnld':
        sigma = 0.2
        C[:,i] *= s
    elif regions[i][1] == 'Antar':
        if regions[i+1][1] == 'Ocean' or regions[i-1][1] == 'Ocean':
            sigma = 0.1
            C[:,i] *= s
#        elif xhat_red[i]*xhat_red[i+1]<0 or  xhat_red[i]*xhat_red[i-1]<0:
#            sigma = 0.05
#            C[:,i] *= s
        else:
            sigma = 0.2
            C[:,i] *= s 
    elif regions[i][1] == 'Alask':
        C[:,i] *= 0.2
        
AtWA = data_AtWA 
VCV = np.linalg.inv(AtWA + C) 
AtWb = data_AtWB[:,1]

xhat = np.dot(VCV,AtWb)
xhat_red = xhat [:-336]

lat = data_msc [:,1]
lon = data_msc [:,2]

fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

#mesh = ax.scatter(lon,lat,c=xhat_red, s=40, norm = norm, cmap='seismic_r', vmin=-0.5, vmax=0.25)
mesh = ax.scatter(lon,lat,c=xhat_red, s=40, norm = norm, cmap='seismic_r')
plt.title('Region-specific regularization of MASCON solution', fontsize=16)
bar = plt.colorbar(mesh, orientation='vertical')

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

#Using custoimized colour bar to improve the visualization of mass change
fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

mesh = ax.scatter(lon,lat,c=xhat_red, s=40, norm = norm_customized, cmap=cmap)
plt.title('Adjusted Region-specific regularization of MASCON solution', fontsize=16)
bar = plt.colorbar(mesh, orientation='vertical')

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

#(iii) What is your best estimate for the gravity field anomalies and 
#how did you regularise your solution to derive your best estimate?

print("Ocean: Ocean signal is largerly regularized with a smaller sigma since signals in ocean is mostly dominated by noise. \
Also, Mass change in part of the ocean is not important for the analysis since ocean have mass change\
as a whole. Ocean next to a ice sheet mascon is less regularized since it includes larger amplitude of\
mass change from ice melt and might include meaningful signals. Ocean locates next to another ocean\
mascon which have opposite signals (one positve and one negative) is largely regularzed to reduce\
the effects of striping.")

print("Land: Land is also regularized since noise is obvious in the unregularized solution. \
Nevertheless, land contains useful hydrological signals so it is less regularized than the ocean.")

print("Greenland, Antarctica, Alaska: icesheet regions are only weakly regularized (larger sigma)\
      since it contains significant signals which is \
meaningful for our interpretation. So regularization will easily remove the true signals. \n\
    The signals in Antar is particularly extreme so it is given special consideration: \
If the signal in the mascon (Antar) is in next to an ocean mascon, the signal is less\
regularized since melting or mass change is more possible and have greatly amplitude.") 





