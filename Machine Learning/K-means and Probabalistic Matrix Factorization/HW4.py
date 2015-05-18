# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:19:59 2015

@author: Jordan
"""

import numpy as np
import matplotlib.pyplot as plt


# Problem 1 (k-menas)

mu = np.empty([3,2])
cov = np.empty([3,2,2])
n = 500
pi = [0.2,0.5,0.3]
pi = np.asarray(pi)

mu[0] = [0,0]
mu[1] = [3,0]
mu[2] = [0,3]

cov[0] = [[1,0], [0,1]]
cov[1] = [[1,0], [0,1]]
cov[2] = [[1,0], [0,1]]


def sample(n, w, mu, cov):
    cdf = np.cumsum(w)
    c = np.empty([n, 2])
    for i in xrange(0,n):
        u = np.random.uniform()
        temp = np.where(u < cdf)
        gauss = temp[0][0]
        c[i] = np.random.multivariate_normal(mu[gauss],cov[gauss],1)
    return c
    
data = sample(n, pi, mu, cov)


'''
d1 = np.random.multivariate_normal(mu[0],cov[0],int(n*pi[0]))
d2 = np.random.multivariate_normal(mu[1],cov[1],int(n*pi[1]))
d3 = np.random.multivariate_normal(mu[2],cov[2],int(n*pi[2]))
data = np.concatenate((d1,d2,d3))
'''


def kmeans(data, obs, clusters):    
    lik = []
    
    c_old = np.zeros([obs]) - 1
    
    mu = np.empty([clusters, np.shape(data)[1]])
    
    temp = np.random.random_integers(0, np.shape(data)[0]-1, clusters)
    
    for k in xrange(0, clusters):
        mu[k] = data[temp[k]]
    
    #mu = np.random.uniform(-10, 10, (clusters, 2))
    
    c = np.empty([obs])
    
    n = np.zeros([clusters])

    
    while not np.array_equiv(c_old,c):
        c_old = np.copy(c)
        
        for i in xrange(0,obs):
            temp = np.sum(np.power(data[i] - mu[0],2))
            c[i] = 0
            for k in xrange(1,clusters):
                 if np.sum(np.power(data[i] - mu[k],2)) < temp:
                     temp = np.sum(np.power(data[i] - mu[k],2))
                     c[i] = k
                     
        for k in xrange(0, clusters):
            n[k] = (c==k).sum()
            temp = np.zeros([np.shape(data)[1]])
            for i in xrange(0, obs):
                if c[i] == k:
                    temp = temp + data[i]
            mu[k] = temp/n[k]
        
        temp = 0        
        for i in xrange(0, obs):
            for k in xrange(0, clusters):
                if c[i] == k:
                    temp = temp + np.sum(np.power(data[i] - mu[k],2)) 
        lik.append(temp)
        
    if len(lik) < 20:
        lik = lik + [lik[len(lik)-1]] * (20 - len(lik))        
        
    return c, mu, lik
    

fig = plt.figure() 

cluster, mu, lik = kmeans(data, n, 2)
plt.subplot(2,2,1)
plt.plot(lik)
plt.xlabel('Iteration')
plt.ylabel('Likelihood')
plt.title('K=2')

cluster, mu, lik = kmeans(data, n, 3)
plt.subplot(2,2,2)
plt.plot(lik)
plt.xlabel('Iteration')
plt.ylabel('Likelihood')
plt.title('K=3')

cluster, mu, lik = kmeans(data, n, 4)
plt.subplot(2,2,3)
plt.plot(lik)
plt.xlabel('Iteration')
plt.ylabel('Likelihood')
plt.title('K=4')

cluster, mu, lik = kmeans(data, n, 5)
plt.subplot(2,2,4)
plt.plot(lik)
plt.xlabel('Iteration')
plt.ylabel('Likelihood')
plt.title('K=5')


fig = plt.figure()
  
cluster, mu, lik = kmeans(data, n, 3)
plt.subplot(1,2,1)
plt.scatter(data[:,0], data[:,1], c = cluster)
plt.title('K=3')

cluster, mu, lik = kmeans(data, n, 5)
plt.subplot(1,2,2)
plt.scatter(data[:,0], data[:,1], c = cluster)
plt.title('K=5')



# Problem 2 (matrix factorization)

ratings = np.loadtxt('movies_csv/ratings.txt', delimiter=",")
ratings_test = np.loadtxt('movies_csv/ratings_test.txt', delimiter=",")
f = open('movies_csv/movies.txt')
movies = f.readlines()
f.close()

for i in xrange(0, len(movies)):
    movies[i] = movies[i].strip()

M = np.zeros([943,1682])
M_test = np.zeros([943,1682])

N1 = np.shape(M)[0]
N2 = np.shape(M)[1]

for i in xrange(0, len(ratings)):
    M[ratings[i][0]-1][ratings[i][1]-1] = ratings[i][2]
    
for i in xrange(0, len(ratings_test)):
    M_test[ratings_test[i][0]-1][ratings_test[i][1]-1] = ratings_test[i][2]
    
omega = []
    
for i in xrange(0,N1):
    for j in xrange(0,N2):
        if M[i][j] != 0:
            omega.append((i,j))
            
omega_test = []
    
for i in xrange(0,N1):
    for j in xrange(0,N2):
        if M_test[i][j] != 0:
            omega_test.append((i,j))


omegau = {}
omegav = {}

for (i,j) in omega:
    if i in omegau.keys():
        omegau[i].append(j)
    else:
        omegau[i] = [j]
    if j in omegav.keys():
        omegav[j].append(i)
    else:
        omegav[j] = [i]
            
var = 0.25
d = 20
I = np.identity(d)
lamb = 10
t1 = lamb*var*I

mean = np.zeros([d])
v = np.empty([N2,d])
u = np.empty([N1,d])

for j in xrange(0, N2):
    v[j] = np.random.multivariate_normal(mean,(1/float(lamb))*I)

def predict(u, v):
    product = np.dot(u, v)
    if product < 1:
        pred = 1.0
    elif product > 5:
        pred = 5.0
    else:
        pred = round(product)
    return pred

RMSE = []
loglik = [] 
           
for iter in xrange(0,100):
    print iter
    for i in xrange(0, N1):
        sum1 = np.zeros([20,20])
        sum2 = np.zeros(20)
        if i in omegau.keys():
            for j in omegau[i]:
                sum1 = sum1 + np.outer(v[j],np.transpose(v[j]))
                sum2 = sum2 + np.dot(M[i][j],v[j])
            u[i] = np.dot(np.linalg.inv(t1 + sum1), sum2)
               
    for j in xrange(0, N2):
        sum1 = np.zeros([20,20])
        sum2 = np.zeros(20)
        if j in omegav.keys():
            for i in omegav[j]:
                sum1 = sum1 + np.outer(u[i],np.transpose(u[i]))
                sum2 = sum2 + np.dot(M[i][j],u[i])
            v[j] = np.dot(np.linalg.inv(t1 + sum1), sum2)
    
    sum3 = 0        
    for (i,j) in omega_test:
        prediction = predict(u[i], v[j])
        actual = M_test[i][j]
        sum3 = sum3 + (prediction - actual)**2
    temp = (sum3/float(len(omega_test)))**0.5
    RMSE.append(temp)
    
    sum4 = 0
    for (i, j) in omega:
        sum4 = sum4 + 0.5/var*np.power(M[i][j] - np.dot(u[i], v[j]),2)
    sum4 = -sum4
    sum5 = 0
    for i in xrange(0, N1):
        sum5 = sum5 + 0.5*lamb*np.sum(u[i]**2)
    sum5 = -sum5
    sum6 = 0
    for j in xrange(0, N2):
        sum6 = sum6 + 0.5*lamb*np.sum(v[j]**2)
    sum6 = -sum6
    loglik.append(sum4+sum5+sum6)

# Part 1: RMSE and likelihood
fig = plt.figure()         
# RMSE 
plt.subplot(1,2,1)      
plt.plot(RMSE)
plt.xlabel('Iteration')
plt.ylabel('RMSE')

# Log Joint Likelihood
plt.subplot(1,2,2) 
plt.plot(loglik)
plt.xlabel('Iteration')
plt.ylabel('Log Joint Likelihood')

from operator import itemgetter

# Part 2: Pick 3 movies and show 5 closest movies to each
# Movie 0 (Toy Story)
movie = 0
distance = {}
for j in xrange(0, N2):
    distance[j] = np.sum((v[movie] - v[j])**2)**0.5
sorted_distance = sorted(distance.items(), key = itemgetter(1))

print 'Movie: ', movies[movie]
print 'Closest movies and distances:'
for i in xrange(0,5):
    print movies[sorted_distance[i+1][0]], ' ', sorted_distance[i+1][1]

# Movie 63 (Shawshank)
movie = 63
distance = {}
for j in xrange(0, N2):
    distance[j] = np.sum((v[movie] - v[j])**2)**0.5
sorted_distance = sorted(distance.items(), key = itemgetter(1))

print 'Movie: ', movies[movie]
print 'Closest movies and distances:'
for i in xrange(0,5):
    print movies[sorted_distance[i+1][0]], ' ', sorted_distance[i+1][1]

# Movie 117 (Twister)
movie = 117
distance = {}
for j in xrange(0, N2):
    distance[j] = np.sum((v[movie] - v[j])**2)**0.5
sorted_distance = sorted(distance.items(), key = itemgetter(1))

print 'Movie: ', movies[movie]
print 'Closest movies and distances:'
for i in xrange(0,5):
    print movies[sorted_distance[i+1][0]], ' ', sorted_distance[i+1][1]


# Part 3: K-means clustering
cluster, centroid, lik = kmeans(u, 943, 30)


for i in xrange(0,5):
    print 'Centroid: ', i
    score = {}
    for j in xrange(0, N2):
        score[j] = np.dot(centroid[i], v[j])
    sorted_score = sorted(score.items(), key = itemgetter(1), reverse=True)
    for i in xrange(0,10):
        print movies[sorted_score[i][0]]
    print '\n'
    
