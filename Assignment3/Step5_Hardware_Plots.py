#Govind | Assignment 3 | 809T
import numpy as np
import matplotlib.pyplot as plt

timeElapsedlist = [] #creating empty list
#opening the text file and extracting the 5th column
with open('hw3data.txt') as f:  #opening the text file
    for line in f:
        timeElapsedlist.append(float(line[0:15])) #extracting the first 15 digits of the float number for calculation
        
# # Graph 1

x = np.linspace(1,len(timeElapsedlist),len(timeElapsedlist)) #determining the x axis
y = timeElapsedlist  #determining the y axis
plt.figure(1)# initializing the first figure
plt.plot(x,y,color='r',linewidth=1.0,label='Raw data') #plotting
plt.title('Object Tracking Processing Time') #assigning plot title
plt.xlabel('Frame') #assigning x label
plt.ylabel('Processing time [msec]') #assigning y label
plt.legend(loc="upper right")#assigning legend and position of the legend
plt.show() #showing the plot


# # Graph 2


plt.figure(2)# initializing the second figure
plt.title('Object Tracking Processing Time') #assigning plot title
plt.xlabel('Processing time [msec]') #assigning x label
plt.ylabel('Frame') #assigning y label
x = timeElapsedlist#determining the x axis
num_bins = len(timeElapsedlist) #The number of bars in the histogram can be tweaked here
n, bins, patches = plt.hist(x, num_bins, facecolor='k', alpha=0.5) #plotting the histogram
plt.show() #showing the plot