timeElapsedlist = []
#opening the text file and extracting the 5th column
with open('hw3data.txt') as f: 
    for line in f:
        timeElapsedlist.append(float(line[0:15]))
#         count= count + 1 #incrementing count


# In[100]:


timeElapsedlist


# In[108]:


timeElapsed = np.array(timeElapsedlist)


# In[109]:


length_of_time = len(timeElapsedlist)


# # Graph 1

# In[110]:


x = np.linspace(1,len(timeElapsedlist),len(timeElapsedlist))
y = timeElapsed
plt.figure(1)
plt.plot(x,y,color='r',linewidth=1.0,label='Raw data') #plotting
plt.title('Object Tracking Processing Time') #assigning plot title
plt.xlabel('Frame') #assigning x label
plt.ylabel('Processing time [msec]') #assigning y label
plt.legend(loc="upper right")#assigning legend and position of the legend
plt.show() #showing the plot


# # Graph 2

# In[111]:


plt.figure(2)
plt.title('Object Tracking Processing Time') #assigning plot title
plt.xlabel('Processing time [msec]') #assigning x label
plt.ylabel('Frame') #assigning y label
x = timeElapsed
num_bins = len(timeElapsedlist)
n, bins, patches = plt.hist(x, num_bins, facecolor='k', alpha=0.5)
plt.show()


# In[ ]:




