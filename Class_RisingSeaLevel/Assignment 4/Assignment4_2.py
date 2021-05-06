"""
@author: Ka Hei
Assignment 4

"""
#import packages needed for the analysis and plotting
import cartopy.crs as ccrs
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.colors import Normalize
import cartopy.feature as cfeature

#Define  function to shift colour bar for plotting
#class MidpointNormalize(Normalize):
#    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
#        self.midpoint = midpoint
#        Normalize.__init__(self, vmin, vmax, clip)
#
#    def __call__(self, value, clip=None):
#
#        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
#        return np.ma.masked_array(np.interp(value, x, y))
#    
#norm = MidpointNormalize(midpoint=0)

#Setting up a customized colour bar for use in (iii)
cmap = plt.cm.jet_r 
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

bounds_i = np.linspace(-500, 500, 20)
bounds_ii = np.linspace(-1, 1, 20)
bounds_iii = np.linspace(-0.25, 0.25, 20)
norm_i = mpl.colors.BoundaryNorm(bounds_i, cmap.N)
norm_ii = mpl.colors.BoundaryNorm(bounds_ii, cmap.N)
norm_iii = mpl.colors.BoundaryNorm(bounds_iii, cmap.N)

#(i) derive and plot the unregularised solution for the gravity field anomalies for this 15-day period
#import data from the file

#Least square method: import AtWA and AtWB
data_AtWA=np.loadtxt('AtWA.data', skiprows = 2)
data_AtWB=np.loadtxt('AtWB.data')
data_msc=np.loadtxt('mascons.latlon')

with open('mascons.regions', 'r') as f:
    x = f.readlines()
regions=[]
for s in range(len(x)):
    regions += [x[s].strip(' ').strip('\n').split(' ')]  
#print(regions)
    
#invert AtWA
VCV = np.linalg.inv(data_AtWA)
AtWb = data_AtWB[:,1]
AtWb.shape

#print(AtWb[:-336,:-336])

xhat = np.dot(VCV,AtWb) #mascon solution
xhat_red = xhat [:-336] #reduced mascon solution to exclude 336 orbital parameters

lat = data_msc [:,1] # setting up lonitude and latitude
lon = data_msc [:,2]

#plotting the unregularised solution for the gravity field anomalies for this 15-day period
fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())
#mesh = ax.scatter(lon,lat,c=xhat_red, s=30, cmap= "seismic_r", vmin=-500, vmax=500)
mesh = ax.scatter(lon,lat,c=xhat_red, s=30,norm =norm_i, cmap= cmap)
bar = plt.colorbar(mesh, orientation='vertical')

ax.coastlines()

#(ii) derive and plot your best global estimate of the mass changes 
#a. using Tikhonov regularisation (Assign same value for every region)

#setting up a C matrix for the regularization
C = np.identity(7863)
for i in range(7527):
    C[:,i] *= 8000 #Setting a value of 8000 in the regularized solution

AtWA = data_AtWA 
VCV = np.linalg.inv(AtWA + C) #including C matrix in the least square solution
AtWb = data_AtWB[:,1]

xhat = np.dot(VCV,AtWb)
xhat_red = xhat [:-336]

lat = data_msc [:,1]
lon = data_msc [:,2]

fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

mesh = ax.scatter(lon,lat,c=xhat_red, s=30, norm = norm_ii, cmap=cmap,  vmin=-1, vmax=1)
bar = plt.colorbar(mesh, orientation='vertical')

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

print("")

#b. using region-specific regularisation. What values did you assign to each region?

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
        sigma = 0.042
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

mesh = ax.scatter(lon,lat,c=xhat_red, s=40, norm = norm_iii, cmap=cmap)

bar = plt.colorbar(mesh, orientation='vertical')

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

#(iii) What is your best estimate for the gravity field anomalies and 
#how did you regularise your solution to derive your best estimate?

print("    Ocean signal is largerly regularized with a smaller sigma since signals in ocean is mostly dominated by noise. \
Also, Mass change in part of the ocean is not important for the analysis since ocean have mass change\
as a whole. Land is also regularized since noise is obvious in the unregularized solution. \
Nevertheless, land contains useful hydrological signals so it is less regularized than the ocean.\
Regions of icesheet is only weakly regularized (larger sigma) since it contains significant signals which is \
meaningful for our interpretation. So regularization will easily remove the true signals. \n\
    The signals in Antar is particularly extreme so it is given special consideration: \
If the signal in the mascon (Antar) is in next to an ocean mascon, the signal is less\
regularized since melting or mass change is more possible and have greatly amplitude.") 



