# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:34:50 2019

@author: Ka Hei Pinky, Chow
"""
###################(i)########################
import numpy as np
import matplotlib.pyplot as plt
import math

print('i) Derive a numerical model to fit the observations. All parameters of your model must be estimated. Plot\
 the observations, overlaid with your modelled values')
    
data=np.loadtxt('Historical_CO2_level_Hawaii.txt',skiprows=4)
# y = ax**2 + mx + c
x=data[:,2]
y=data[:,4]
n_obs = len(x) 
n_params = 3 

#print(len(x))
#print(len(y))

#y = Nx**2 + Mx + F*cos(wx+phi) + G 
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

y_modelled = np.zeros((n_obs))
for i in range(n_obs):
    y_modelled[i] = N*x[i]**2+M*x[i]+F*math.cos(w*x[i]+phi)+G
    
plt.figure(figsize=(10,7.5))

plt.plot(x,y,'o') #the observations
plt.plot(x,y_modelled,'red',linewidth=2.0) #modelled values
plt.title('Estimations of CO2 level in Hawaii', fontsize=18)
plt.xlabel('Year', fontsize=20)
plt.ylabel('CO2 level im ppm', fontsize=20)

plt.show() 

###################(ii)#######################
print("\n(ii) What is the root-mean-square of your modelled values with respect to the observations?")
rms = np.sqrt((sum((y_modelled - y)**2))/len(y))
print('The root-mean-square is: ', round(rms,3), "(round up to 3 decimal places)")

###################(iii)#######################
print("\n(iii) What is the acceleration of CO2 content in the Earth’s atmosphere?")
print("The function of the modelled curve is: y = Nx^2 + Mx + F cos(wx+phi) + G ")
print("\nTo calculate acceleration, seasonal variation can be ignored, which is \
      represented by the component F cos(wx+phi) in the function.")

print("Derivative of the remaining component = 2Nx + M")
print("Acceleration = ", round(2*N,4), "ppm per year")

###################(iv)#######################
 #y = N*x[i]**2+M*x[i]+F*math.cos(w*x[i]+phi)+G
print("To simplfy the function, the component of seasonal variation is removed first. It will be considered afterwards")
print("The function becomes: y = Nx^2 + Mx + G")
print("When y = 500,")

delta = M**2 - 4*N*(G-500)
#print(delta)
critical_point_A = (-M + np.sqrt(M**2 - 4*N*(G-500)))/(2*N)
critical_point_B = (-M - np.sqrt(M**2 - 4*N*(G-500)))/(2*N)

print("The solution is/are: ")
if critical_point_A > 1960:
    print(critical_point_A)
if critical_point_B > 1960:
    print("\n",critical_point_B)

####Two direction approximation
#1

w=2 * np.pi
N=  0.01268834460156718
M=  -48.9089981020247
F=  -2.820479857751829
phi=  1.2067796269235234
G=  47433.974575281914

print("\nWhen x=2065,")
YMAX = N*2065**2+M*2065+F*math.cos(w*2065+phi)+G
print("YMAX = ",YMAX)
if YMAX > 500 + F:
    print("\nThe year which pass 500ppm for the last time is no later than 2065.")
else:
    print("The year which pass 500ppm for the last time is later than 2065.")

#print(Calculation)
Left_Limit = 0
i = 2045
while (Left_Limit < 500):
    Left_Limit = N*(i**2)+M*i+F*math.cos(w*i+phi)+G
    i += 0.01
print("\nThe approximation of x from the left side is:", round(i,3))
    
#2
h = 2065
Right_Limit = N*(h**2)+M*h+F*math.cos(w*h+phi)+G
while (Right_Limit > 500):
    Right_Limit = N*(h**2)+M*h+F*math.cos(w*h+phi)+G
    h -= 0.01
print("The approximation of x from the right side is:", round(h,3))

print("\nThus, the year when the CO2 level pass 500 ppm for the last time is: \n>>>>>>Year", 
      int(h),",",int((h%1)*12),"th month")

























