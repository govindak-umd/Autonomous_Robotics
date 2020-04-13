#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from matplotlib import pyplot as plt


# In[2]:


all_gpio_val = []
file1 = open("gpio_values.txt","r") 
content = file1.readlines()
for line in content: 
      
    for i in line: 
          
        # Checking for the digit in  
        # the string 
        if i.isdigit() == True: 
              
            all_gpio_val.append(int(i))
file1.close() 


# In[3]:


all_gpio_val_2 = []
file1 = open("gpio_values_2.txt","r") 
content = file1.readlines()
for line in content: 
      
    for i in line: 
          
        # Checking for the digit in  
        # the string 
        if i.isdigit() == True: 
              
            all_gpio_val_2.append(int(i))
file1.close()


# In[5]:


x = np.linspace(0,len(all_gpio_val),len(all_gpio_val)+1)
x = list(x)
x.pop()


# In[7]:


x2 = np.linspace(0,len(all_gpio_val_2),len(all_gpio_val_2)+1)
x2 = list(x2)
x2.pop()


# In[9]:


plt.plot(x,all_gpio_val,'r')
plt.plot(x,all_gpio_val_2,'b')
plt.title('Motor Encoder Analysis - Baron')
plt.savefig('motor_encoder_graph.png')
plt.xlabel('GPIO Input Reading')
plt.ylabel('Encoder State : Baron')
plt.show()


# In[ ]:




