"""
@author: Ka Hei
Assignment 4

"""
#Import packages needed for the analysis and plotting
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

#Setting up a customized colour bar for the visual adjustment in part (iii)
cmap = plt.cm.jet_r 
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(-0.25, 0.25, 20)
norm_customized = mpl.colors.BoundaryNorm(bounds, cmap.N)


#(i) derive and plot the unregularised solution for the gravity field anomalies for this 15-day period

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

xhat = np.dot(VCV,AtWb) #mascon solution with orbital parameters
xhat_red = xhat [:-336] #reduced mascon solution to exclude 336 orbital parameters

lat = data_msc [:,1] #setting up lonitude and latitude
lon = data_msc [:,2]

#plotting the unregularised solution for the gravity field anomalies for this 15-day period
      
fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())
mesh = ax.scatter(lon,lat,c=xhat_red, s=30, cmap= "seismic_r", vmin=-500, vmax=500)

plt.title('Unregularized MASCON solution', fontsize=16)
bar = plt.colorbar(mesh, orientation='vertical')

ax.coastlines()
      
print("(i) From the plotting, extreme signals can be seen in Antarctica, Greenland and Africa. \
      Yet, regional pattern cannot be observed. It includes large noise, both positive and negative\
      in the plot.\n")

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

#Plotting Tikhonov regularisation
fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

mesh = ax.scatter(lon,lat,c=xhat_red, s=30, norm = norm, cmap='seismic_r', vmin=-1, vmax=1)
bar = plt.colorbar(mesh, orientation='vertical')
plt.title('Tikhonov regularization of MASCON solution', fontsize=16)

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

print("(ii) (a) Values such as 1000, 3000, and 10000 were tried for the C matrix in the solution.\
      If the values are too large, the signals are largely supressed and no clear pattern of\
      of ice melt can be seen from the plot. If the values are too small, the plot is generally\
      underregularized and no clear true signals can be inferred owing to the strong presence of\
      thre noise. At the end, value of 8000 maintain a good balance for the solution. It has \
      reasonable noise. Yet, the striping in the ocean cannot be completely avoided. \n")

#(ii) b. using region-specific regularisation. What values did you assign to each region?
C = np.identity(7863)
#inputing parameters
sigma = 1
n = 14

# Assigning values for regularization
for i in range(1, len(regions)-1):
    s = n/(sigma**2)
    i = int(i)
    if regions[i][1] == 'Ocean':#ocean: 0.015
        sigma = 0.015
        C[:,i] *= s          
    elif regions[i][1] == 'Land': #Land: 0.04
        sigma = 0.04
        C[:,i] *= s
    elif regions[i][1] == 'Grnld': #Greenland: 0.2
        sigma = 0.2
        C[:,i] *= s
    elif regions[i][1] == 'Antar': #Antarctica: 0.2
        sigma = 0.2
        C[:,i] *= s 
    elif regions[i][1] == 'Alask': #Alaska: 0.2
        C[:,i] *= 0.2
        
#Least square method
AtWA = data_AtWA 
VCV = np.linalg.inv(AtWA + C) 
AtWb = data_AtWB[:,1]

xhat = np.dot(VCV,AtWb)
xhat_red = xhat [:-336]

lat = data_msc [:,1]
lon = data_msc [:,2]

#Plotting
fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

mesh = ax.scatter(lon,lat,c=xhat_red, s=40, norm = norm, cmap='seismic_r', vmin=-0.5, vmax=0.25)
plt.title('Region-specific regularization of MASCON solution', fontsize=16)
bar = plt.colorbar(mesh, orientation='vertical')

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

print("(ii) (b) Values assigned for each region: \n\
Ocean: 0.015\n\
Land: 0.04\nGreenland: 0.2\nAlaska: 0.2\nAntarctica: 0.2\n")


#(iii) What is your best estimate for the gravity field anomalies and 
#how did you regularise your solution to derive your best estimate? Justify your choice.

C = np.identity(7863)
#inputing parameters
sigma = 1
n = 14

for i in range(1, len(regions)-1):
    s = n/(sigma**2)
    i = int(i)
    if regions[i][1] == 'Ocean':#Ocean: 0.015; if close to ice sheet: 0.1; stripes: 0.01
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
    elif regions[i][1] == 'Land': #Land: 0.04
        sigma = 0.04
        C[:,i] *= s
    elif regions[i][1] == 'Grnld': #Greenland: 0.2
        sigma = 0.2
        C[:,i] *= s
    elif regions[i][1] == 'Antar': #Antarctica: 0.2; if next to ocean: 0.1
        if regions[i+1][1] == 'Ocean' or regions[i-1][1] == 'Ocean':
            sigma = 0.1
            C[:,i] *= s
        else:
            sigma = 0.2
            C[:,i] *= s 
    elif regions[i][1] == 'Alask': #Alaska: 0.2
        C[:,i] *= 0.2
        
#Least square method
AtWA = data_AtWA 
VCV = np.linalg.inv(AtWA + C) 
AtWb = data_AtWB[:,1]

xhat = np.dot(VCV,AtWb)
xhat_red = xhat [:-336]

lat = data_msc [:,1]
lon = data_msc [:,2]

#Using custoimized colour bar to improve the visualization of mass change
fig1 = plt.figure(figsize=(15,8))
ax = plt.axes(projection=ccrs.PlateCarree())

mesh = ax.scatter(lon,lat,c=xhat_red, s=40, norm = norm_customized, cmap=cmap, vmin=-0.5, vmax=0.25)
plt.title('Adjusted Region-specific regularization of MASCON solution', fontsize=16)
bar = plt.colorbar(mesh, orientation='vertical')

ax.add_feature(cfeature.OCEAN, alpha=0.1, zorder = 1)
ax.coastlines()

print("(iii) Values assigned for each region: \n\
Ocean: 0.015; next to ice sheet: 0.1; appearence of stripes: 0.01\n\
Land: 0.04\nGreenland: 0.2\nAlaska: 0.2\nAntarctica: 0.2; next to ocean: 0.1 \n")

print("Above show the best estimation of the gravity field anomalies.")
print("\nOcean: In order to get the best estimate, ocean signal is largerly regularized with a smaller sigma since signals in ocean is mostly dominated by noise. \
Also, Mass change in part of the ocean is not important for the melting icesheet analysis, \
Especially icesheet far away from the icesheet. Regional pattern of ocean mascon far from the\
 icesheet have less significance and might includes mostly noise.\
Ocean next to a ice sheet mascon is less regularized since it might includes large amplitudes of\
mass change from the ice melt and hence includes meaningful signals. Ocean locates next to another ocean\
mascon which have opposite signals (one positve and one negative) is largely regularzed to reduce\
the effects of striping.")

print("\nLand: Land is moderately regularized since noise is obvious in the unregularized solution. \
Nevertheless, land contains useful hydrological signals so it is less regularized than the ocean.")

print("\nGreenland, Antarctica, Alaska: icesheet regions are only weakly regularized (larger sigma)\
      since it contains significant signals which is \
meaningful for our interpretation. Large regularization will remove the true signals. \n\
The signals in Antarctica is particularly strong so it is given special consideration: \
If the signal in the Antarctica mascon is in next to an ocean mascon, the signal is less\
regularized since melting or mass change is more possible and has greater amplitude.") 




















