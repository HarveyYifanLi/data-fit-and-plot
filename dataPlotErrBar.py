# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 15:10:33 2014

@author: YIFAN LI
"""
############################################################
#
# comments are explaining the following line of code
#
# AFTER a line of code, there can be multiple of the following lines that further explain the ABOVE line of code:
## <-- explains used function parameters. For additional information see the object inspector (help panel on the upper right)   
#### <-- this marks additional information that explain some of the inner workings of python
#
############################################################

# import the usual libraries
import numpy as np
import matplotlib.pyplot as plt

# read in data - the file is assumed to be in csv format (separated by comma). Files need to be specified with a full path OR they have to be saved in the same folder as the script
data = np.loadtxt('copper2a.csv', delimiter=',', comments='#')

# access the data columns and assign variables x,y,x_sigma,y_sigma
x = data[:,0]
y = data[:,2]
x_sigma = data[:,1]
y_sigma = data[:,3]
nsine=0
maxsinesum=0
maxsine=0
#### data is not copied during this process - x,y,x_sigma,y_sigma are 'pointing' to the same memory as data
##define a for loop to calculate the number of sine full periods of the voltage that appears.
# plot the data with errorbars
for i in range(y.shape[-1]):
    if x[i]>=30 and x[i]<=61.4:
        
        if y[i]>= 4.05:
            nsine= nsine+1
            maxsinesum+=y[i]
maxsine=maxsinesum/nsine 
print(maxsine)


nsine=0
for i in range(y.shape[-1]):
    if x[i]>=30 and x[i]<=61.4:
        
        if y[i]>= maxsine:
            nsine= nsine+1

print(nsine)   
    
plt.errorbar(x, y,xerr=x_sigma,yerr=y_sigma,marker='.',linestyle='')
## xerr=x_sigma,yerr=y_sigma : assign the data for the error bars in x- and y-direction
## marker='o' : use markers to indicate each data point (x_1,y_1),(x_2,y_2)
## linestyle= '' : no line is drawn to connect the data points

# add axis labels
plt.xlim(30,62)
plt.ylim(2.0,4.5)

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
# ----- you can save a figure by right-clicking on the graph in the console
# ----- alternatively use: plt.savefig("NAMEOFFIGURE")