m# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:18:55 2019
"""

from __future__ import division
from numpy import linspace, loadtxt, ones, convolve
import numpy as np
import matplotlib.pyplot as plt
import math


###########(i)#############
print('(i) Derive a model to represent the observations. Plot the observations along with \
      your modelled values.')

data=np.loadtxt('sl_global_Seasonal_Variation_retained.txt',skiprows=1)
# y = ax**2 + mx + c
x=data[:,0]
y=data[:,1]
n_obs = len(x) 
n_params = 3 

a=1
m=1
c=0

A = np.zeros((n_obs,n_params))
b = np.zeros((n_obs))
xhat = np.zeros((n_params))

for iter in range(20):
    for i in range(n_obs): 
        A[i,0] = x[i]**2
        A[i,1] = x[i]
        A[i,2] = 1.0
        b[i] = y[i] - (a*x[i]**2+m*x[i]+c)
        
    At = np.transpose(A)
    AtA = np.dot(At,A)
    VCV = np.linalg.inv(AtA) 
    Atb = np.dot(At,b)
    xhat = np.dot(VCV,Atb)     
  
    a = a + xhat[0]
    m = m + xhat[1]
    c = c + xhat[2]        
            
print("Final parameter estimates:   a= ",a)
print("Final parameter estimates:   m= ",m)
print("Final Parameter estimates:   c= ",c) 

y_modelled = np.zeros((n_obs))
for i in range(n_obs):
    y_modelled[i] = a*x[i]**2 + m*x[i] + c 

plt.figure(figsize=(10,7.5))

plt.plot(x,y,'o') #the observations
plt.plot(x,y_modelled,'red', linewidth=2.0) #modelled values
plt.title('Estimations of Global Sea Level Change from Satellite Altimetry', fontsize=18)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Sea level rise in mm', fontsize=20)

plt.show() 

###########(ii)#############
print('(ii) What is the linear rate (and uncertainty) of sea level rise over the altimeter period n\
      derived from these observations?')

slope_data = np.gradient(x,y_modelled)
slope_modelled = np.mean(slope_data)
print('Linear rate of sea level rise = Slope of trendline = ', slope_modelled)

###########(iii)#############
print('\n(iii) Is there a statistically significant acceleration in sea level rise?')
#Use F-Test
"""calculate SSRur/ Step 2: calculate SSRr /Step 3: determine values for q, n and k /
Step 4: calculate F0/ Step 5: choose a confidence level, and look up f-distribution tables 
to find value Fq,n-(k+1)/ Step 6: Compare F0 and Fq,n-(k+1)
"""
#Establish the reduced model
#y = c
print("By examining the statistical significance of parameter acceleration, \
      a reduced model without accelation (i.e. Y axis, rate of sea level rise is assumed constant) \
      is established")

data=np.loadtxt('sl_global_Seasonal_Variation_retained.txt',skiprows=1)
x=data[:,0]
y=data[:,1]
n_obs = len(x) 
n_params = 2 

m=1
c=0
A = np.zeros((n_obs,n_params))
b = np.zeros((n_obs))
xhat = np.zeros((n_params))

for iter in range(20):
    for i in range(n_obs): 
        A[i,0] = x[i]
        A[i,1] = 1.0
        b[i] = y[i] - (m*x[i]+c)
        
    At = np.transpose(A)
    AtA = np.dot(At,A)
    VCV = np.linalg.inv(AtA) 
    Atb = np.dot(At,b)
    xhat = np.dot(VCV,Atb)     
    m = m + xhat[0]
    c = c + xhat[1]    
        
print("Final parameter estimates:   Slope:",m)
print("Final Parameter estimates: Y-offset:",c) 

y_rmodelled = np.zeros((n_obs))
for i in range(n_obs):
    y_rmodelled[i] = m*x[i] + c 

plt.figure(figsize=(10,7.5))
plt.plot(x,y,'o') #the observations
plt.plot(x,y_rmodelled,'red', linewidth=2.0) #modelled values
plt.title('Reduced Model: Estimations of Global Sea Level Change from Satellite Altimetry', fontsize=18)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Sea level rise in mm', fontsize=20)

plt.show() 

#F test Calculation
SSRfull = sum((y_modelled - y)**2)
SSRreduced = sum((y_rmodelled - y)**2)
print("SSR value for full model is:", SSRfull)
print("SSR value for reduced model is:", SSRreduced)
q = 1
n = len(y)
k = 1
#print(n-k-1)

#calculate F0
F0 = ((SSRreduced - SSRfull)*(n - k - 1))/(q*SSRfull)
print("\nF-test: \nThe calculated value of F0 is ", F0)
print("\nWhen the confidence level is 1% (i.e. alpha = 0.01), F critical value = 6.635;")
if F0 > 6.635:
    print("\nResults: \nThere is statistically significance for the prarameter acceleration in sea level rise.")
else:
    print("\nResults: \nThere is no statistically significance for the parameter acceleration in sea level rise.")


###########(iv)#############
print(' \n (iv) Calculate and plot a 60-day running mean of the values.')

data=loadtxt('sl_global_Seasonal_Variation_retained.txt', float, skiprows=1)

x = data[:,0]
y = data[:,1]

y_sum = np.zeros((len(y)-5))
x_sum = np.zeros((len(y)-5))

for i in range (len(y)-5):
    y_sum[i] = np.sum(y[0+i:6+i])/6
    x_sum[i] = np.sum(x[0+i:6+i])/6
#print(y_sum)
#print(x_sum) 

plt.figure(figsize=(10,7.5))
plt.plot(x,y,'o')
plt.plot(x_sum,y_sum,'red',linewidth=2.0)
plt.title('Rolling average of sea level change', fontsize=18)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Sea level rise in mm', fontsize=20)

plt.savefig('60 days Running Average for the Sea Level Rise')

plt.show()


###########(v)#############
print('(v) What is the amplitude of the annual variation in global sea level?')
print('To find out the annual variation in the global sea level, we need to first discompose the \
      variation form the trend in the data.')

data=np.loadtxt('sl_global_Seasonal_Variation_retained.txt',skiprows=1)

#y = Nx**2 + Mx + F*cos(wx+phi) + G 

#Fitting data into function (2)
x=data[:,0]
y=data[:,1]
n_obs = len(x) 
n_params = 5

#Setting initial vlaues
w=2 * np.pi
N=1
M=1
F=1
phi=1
G=1

A = np.zeros((n_obs,n_params))
b = np.zeros((n_obs))
xhat = np.zeros((n_params))

for iter in range(20):
    for i in range(n_obs): 
        A[i,0] = x[i]**2
        A[i,1] = x[i]
        A[i,2] = np.cos(w*x[i]+phi)
        A[i,3] = -F*np.sin(w*x[i]+phi)
        A[i,4] = 1.0
        b[i] = y[i] - (N*x[i]**2+M*x[i]+F*math.cos(w*x[i]+phi)+G)
        
    At = np.transpose(A)
    AtA = np.dot(At,A)
    VCV = np.linalg.inv(AtA) 
    Atb = np.dot(At,b)
    xhat = np.dot(VCV,Atb)     
  
    N = N + xhat[0]
    M = M + xhat[1]
    F = F + xhat[2]
    phi = phi + xhat[3]
    G = G + xhat[4]       
            
print("Final parameter estimates:   N= ",N)
print("Final parameter estimates:   M= ",M)
print("Final Parameter estimates:   F= ",F) 
print("Final Parameter estimates:   phi= ",phi) 
print("Final Parameter estimates:   G= ",G)

y_SVmodelled = np.zeros((n_obs))
for i in range(n_obs):
    y_SVmodelled[i] = N*x[i]**2+M*x[i]+F*math.cos(w*x[i]+phi)+G

plt.figure(figsize=(10,7.5))

plt.plot(x,y,'o') #the observations
plt.plot(x,y_SVmodelled,'red', linewidth=2.0) #modelled values
plt.title('Estimations of Global Sea Level Change from Satellite Altimetry', fontsize=18)
plt.xlabel('Year', fontsize=20)
plt.ylabel('Sea level rise in mm', fontsize=20)

plt.show() 

print("Thus, the amplitude of the annual variation is:", F)

