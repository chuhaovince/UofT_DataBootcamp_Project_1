#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Modules

import urllib
import json
from pprint import pprint
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# extract all the files from the zip folder to current working directory
from zipfile import ZipFile


# In[2]:


# Get the dataset metadata by passing package_id to the package_search endpoint
# For example, to retrieve the metadata for this dataset:

url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
params = { "id": "8c233bc2-1879-44ff-a0e4-9b69a9032c54"}
response = urllib.request.urlopen(url, data=bytes(json.dumps(params), encoding="utf-8"))
package = json.loads(response.read())
pprint(package)


# In[3]:


# Get the data url for year 2016
filedata_2016_url = package["result"]["resources"][8]["url"]
filedata_2016_url


# In[ ]:


# how to download the file from the above url
import requests
data_2016 = requests.get(filedata_2016_url)


# In[ ]:


#store the downloaded file in the parking2018.zip 
open('Resourses/parking2016.zip', 'wb').write(data_2016.content)


# In[ ]:


# Unzip the zipfile
with ZipFile("Resourses/parking2016.zip","r") as zfile:
    zfile.extractall("Resourses")


# In[2]:


# Create all four pandas data frames
data1 = pd.read_csv("Resourses/Parking_Tags_Data_2016_1.csv")
data2 = pd.read_csv("Resourses/Parking_Tags_Data_2016_2.csv")
data3 = pd.read_csv("Resourses/Parking_Tags_Data_2016_3.csv")
data4 = pd.read_csv("Resourses/Parking_Tags_Data_2016_4.csv")


# In[3]:


# Concatenate all data frames
complete_data = pd.concat([data1,data2,data3,data4])
complete_data.head()


# In[4]:


# Fill the NaN cells with nothing inside it
new_data = complete_data.fillna("")
new_data.head()


# In[5]:


# Group data set by dates
grouped_data = new_data.groupby("date_of_infraction")


# In[6]:


# Show the grouped data
grouped_data.first().head()


# In[53]:


# Get the address at which each infraction took place with date
# Create a blank dictionary to store addresses for specific dates
address_book = {}

# Loop through each date and extract addresses for the same day
for date in grouped_data:
    # Create a blank list to store addresses for the same day
    address = []
    # date_data represent a data set for a specific day, e.g. 20160101
    date_data = pd.DataFrame(date[1]) # Transfer the tuple into data frame
    for index, row in date_data.iterrows():
        # Adding all the addresses up into a list
        if row["location3"] != "":
            # if it is an interscetion of 2 streets
            address.append(str(row["location2"]+" / "+row["location4"])) 
        else:
            # if only a street with unit number
            address.append(str(row["location2"]))
        address_book[date[0]] = address # update the address_book dict, date[0] is the date, e.g. 20160101


# In[25]:


# Organize the data frame by seasons
# From the internet, 
# Spring - March 20 to June 20. Spring is a rainy season in most parts of Ontario. ...
# Summer - June 21 to September 21. ...
# Fall (or Autumn) - September 22 to December 20. ...
# Winter - December 21 to March 19.
spring = new_data.loc[(new_data["date_of_infraction"]>=20160320) & (new_data["date_of_infraction"]<=20160620),:]
summer = new_data.loc[(new_data["date_of_infraction"]>=20160621) & (new_data["date_of_infraction"]<=20160921),:]
fall = new_data.loc[(new_data["date_of_infraction"]>=20160922) & (new_data["date_of_infraction"]<=20161220),:]
winter = new_data.loc[(new_data["date_of_infraction"]>=20161221) | (new_data["date_of_infraction"]<=20160319),:]

# Get total tickets granted for each season
num_tickets_spring = len(spring)
num_tickets_summer = len(summer)
num_tickets_fall = len(fall)
num_tickets_winter = len(winter)


# In[49]:


# Bar chart for seasonal ticketing
plt.bar([1,2,3,4],[num_tickets_spring, num_tickets_summer, num_tickets_fall, num_tickets_winter])
plt.xticks([1,2,3,4],["Spring", "Summer", "Fall", "Winter"])
plt.yticks([100000,200000,300000,400000,500000,600000],["100K","200K","300K","400K","500K","600K"])


# In[35]:


num_tickets_spring


# In[55]:


spring["set_fine_amount"].sum()


# In[69]:


# Discover the 10 kinds of infractions drivers usually get the most
list(new_data.groupby("infraction_description").count().sort_values("tag_number_masked", ascending = False).head(10).index)


# In[ ]:




