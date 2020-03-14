#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scipy import signal

import matplotlib.pyplot as plot


import numpy as np


# In[90]:


t = np.linspace(0, 2, 1000, endpoint=True)

 
plot.plot(t, 1.5+1.5*signal.square(2 * np.pi * t, duty = 0.3),linewidth=7)

 

# Give a title for the square wave plot

plot.title('Forward Motor configuration')
plot.ylabel('A (volts)')
plot.ylim(0, 3)
plot.show()
t = np.linspace(0, 2, 1000, endpoint=True)
plot.ylim(0, 3)

plot.plot(t, 1.5- 1.5*signal.square(2 * np.pi * t, duty = 0.3),linewidth=7)

 
plot.ylim(0, 3)
plot.xlabel('Time in milliseconds with Period 1ms and duty cycle = 0.3(On for A) and off for B ')
plot.ylabel('B (volts)')
plot.show()





# In[96]:


# Sampling rate 1 HZ

t = np.linspace(0, 2, 1000, endpoint=True)

plot.plot(t, 1.5-1.5*signal.square(2 * np.pi * t, duty = 0.7),linewidth=7)

 

# Give a title for the square wave plot

plot.title('Reverse Motor configuration')



plot.ylabel('A (volts)')
plot.ylim(0, 3)
plot.show()
t = np.linspace(0, 2, 1000, endpoint=True)
plot.plot(t, 1.5+1.5*signal.square(2 * np.pi * t, duty = 0.7),linewidth=7)



plot.xlabel('Time in milliseconds with Period 1ms and duty cycle = 0.7(On for B, Off for A) ')

 

# Give y axis label for the square wave plot

plot.ylabel('B volts')

 

# plot.grid(True, which='both')

 

# # Provide x axis and line color

# plot.axhline(y=0, color='k')

 

# # Set the max and min values for y axis

plot.ylim(0, 3)

 

# Display the square wave drawn

plot.show()




