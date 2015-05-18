
# coding: utf-8

# In[9]:

import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import os

# Load Data
business=pd.read_csv('business_json.csv')
reviews=pd.read_csv('reviews_json.csv')
users=pd.read_csv('users_json.csv')


# In[10]:

# Check the Shape
print business.shape
print reviews.shape
print users.shape


# In[11]:

# Check column values of checkin
list(users.columns.values)


# In[12]:

# Check column values of reviews
list(reviews.columns.values)


# In[13]:

list(business.columns.values)
#restaurants=business[business['categories'].str.contains('Restaurants')]
#list(business.columns.values)


# In[25]:

# Get only restaurants in Vegas
restaurants=business[business['categories'].str.contains('Restaurants')]
rest_columbia=restaurants[restaurants['schools'].str.contains('Columbia University')]
reviews_columbia=reviews[reviews['business_id'].isin(rest_columbia['business_id'])]
users_columbia=users[users['user_id'].isin(reviews_columbia['user_id'])]

print restaurants.shape
print rest_columbia.shape
print reviews_columbia.shape
print users_columbia.shape


# In[21]:

import graphlab
sf = graphlab.SFrame({'user_id': list(reviews_columbia['user_id']),
                      'item_id': list(reviews_columbia['business_id']),
                      'rating': list(reviews_columbia['stars'])})
m = graphlab.recommender.factorization_recommender.create(sf,target='rating')
nn = m.get_similar_items(k=30)


# In[22]:

b=nn.to_dataframe()


# In[23]:

b.to_csv('MF.csv')

