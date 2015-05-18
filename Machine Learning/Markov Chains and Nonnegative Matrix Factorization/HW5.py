# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:30:47 2015

@author: Jordan
"""

import numpy as np
#from scipy import linalg
#from scipy.linalg import eigh as largest_eigh
import matplotlib.pyplot as plt
from scipy import ndimage
from sklearn.preprocessing import normalize

# Problem 1 (Markov chains)

scores = np.loadtxt('hw5text/cfb2014scores.csv', delimiter=",")
scores[:,0] = scores[:,0] - 1
scores[:,2] = scores[:,2] - 1


f = open('hw5text/legend.txt')
schools = f.readlines()
f.close()

for i in xrange(0, len(schools)):
    schools[i] = schools[i].strip()
    
M = np.zeros([759,759])

w = np.empty([len(scores),len(M)])
#w[0] = np.random.uniform(size=len(M))
w[0] = np.ones(759)/float(759)  

for i in xrange(0,len(scores)):
    index1 = scores[i][0]
    index2 = scores[i][2]
    points1 = scores[i][1]
    points2 = scores[i][3]
    indicator1 = 0
    indicator2 = 0
    if points1 > points2:
        indicator1 = 1
    if points1 < points2:
        indicator2 = 1
    
    M[index1][index1] = M[index1][index1] + indicator1 + points1/(points1+points2)
    M[index2][index2] = M[index2][index2] + indicator2 + points2/(points1+points2)
    M[index1][index2] = M[index1][index2] + indicator2 + points2/(points1+points2)
    M[index2][index1] = M[index2][index1] + indicator1 + points1/(points1+points2)
    

 
 
for i in xrange(0,len(M)):
    row = M[i]
    rowsum = sum(row)
    for j in xrange(0, len(row)):
        M[i][j] = M[i][j]/rowsum

w = np.empty([1001,len(M)])
#w[0] = np.random.uniform(size=len(M))    
w[0] = np.ones(759)/float(759)    
for i in xrange(0, 1000):
    w[i+1] = np.dot(w[i],M)

for t in [10,100,200,1000]:
    sortvals = np.sort(w[t])[::-1]
    sortinds = np.argsort(w[t])[::-1]
    print 't = ' + str(t)
    for i in xrange(0,20):
        print str(schools[sortinds[i]]) + ' ' + str(sortvals[i])
    print '\n'

#la,v = linalg.eig(np.transpose(M))
la,v = np.linalg.eig(np.transpose(M))
#la, v = largest_eigh(np.transpose(M), eigvals=(759-1,759-1))
u1 = v[:,np.argmax(la)]


tempsum = sum(u1)
for i in xrange(0,len(u1)):
    u1[i] = u1[i]/tempsum    


norm = []
for t in xrange(0,1000):
    norm.append(np.sum(abs(w[t]-u1)))
plt.plot(norm)
plt.xlabel('Iteration')
plt.ylabel('L1 norm of W[t] - W[inf]')
norm[999]
    



# Problem 2 (Nonnegative matrix factorization)

# Part 1

X_faces = np.loadtxt('hw5text/faces.csv', delimiter=",")
W_faces = np.random.uniform(size=[1024,25])
H_faces = np.random.uniform(size=[25,1000])

obj1 = []
for t in xrange(0,200):
    H_faces = H_faces * (np.dot(np.transpose(W_faces),X_faces)) / ((np.dot(np.dot(np.transpose(W_faces),W_faces), H_faces)) + 10**(-16))
    W_faces = W_faces * (np.dot(X_faces,np.transpose(H_faces))) / ((np.dot(np.dot(W_faces,H_faces), np.transpose(H_faces))) + 10**(-16))
    temp = np.sum(np.power(X_faces - np.dot(W_faces,H_faces),2))
    obj1.append(temp)

# Plot objective function
plt.plot(obj1)
plt.xlabel('Iteration')
plt.ylabel('Objective function')
plt.title('Faces with Euclidean Penalty')

# 3 images
#Image 1
plt.subplot(321)
image = X_faces[:,0]
image = ndimage.rotate(image.reshape(32,32), -90, reshape=False)
plt.imshow(image)
plt.title('Image 1')

plt.subplot(322)
H_column = H_faces[:,0]
col = np.argmax(H_column)
W_column = W_faces[:,col]
image1 = ndimage.rotate(W_column.reshape(32,32), -90, reshape=False)
plt.imshow(image1)
plt.title('Column of W: ' + str(col))


#Image 2
plt.subplot(323)
image = X_faces[:,10]
image = ndimage.rotate(image.reshape(32,32), -90, reshape=False)
plt.imshow(image)
plt.title('Image 2')

plt.subplot(324)
H_column = H_faces[:,10]
col = np.argmax(H_column)
W_column = W_faces[:,col]
image1 = ndimage.rotate(W_column.reshape(32,32), -90, reshape=False)
plt.imshow(image1)
plt.title('Column of W: ' + str(col))

#Image 3
plt.subplot(325)
image = X_faces[:,100]
image = ndimage.rotate(image.reshape(32,32), -90, reshape=False)
plt.imshow(image)
plt.title('Image 3')

plt.subplot(326)
H_column = H_faces[:,200]
col = np.argmax(H_column)
W_column = W_faces[:,col]
image1 = ndimage.rotate(W_column.reshape(32,32), -90, reshape=False)
plt.imshow(image1)
plt.title('Column of W: ' + str(col))



# Part 2

X_nyt = np.zeros([3012,8447])

f = open('hw5text/nyt_data.txt')
lines = f.readlines()
f.close()

g = open('hw5text/nytvocab.dat')
nytworddict = g.read().splitlines()
g.close()

doc = 0
for line in lines:
    idxcnt = line.strip().split(',')
    for word in idxcnt:
        temp = word.split(':')        
        index = int(temp[0]) - 1
        count = int(temp[1])
        X_nyt[index][doc] = count
    doc = doc + 1

W_nyt = np.random.uniform(size=[3012,25])
H_nyt = np.random.uniform(size=[25,8447])

obj2 = []
for t in xrange(0,200):
    print t
    temp1 = normalize(np.transpose(W_nyt), norm='l1', axis=1)
    purple = X_nyt / (np.dot(W_nyt,H_nyt) + 10**(-16))
    H_nyt = H_nyt * np.dot(temp1,purple)
    temp2 = normalize(np.transpose(H_nyt), norm='l1', axis=0) 
    purple = X_nyt / (np.dot(W_nyt,H_nyt) + 10**(-16))
    W_nyt = W_nyt * np.dot(purple,temp2)
    temp = np.sum((X_nyt * np.log(1/(np.dot(W_nyt,H_nyt) + 10**(-16)))) + (np.dot(W_nyt,H_nyt)))
    obj2.append(temp)
  

# Plot objective function
plt.plot(obj2)
plt.xlabel('Iteration')
plt.ylabel('Objective function')
plt.title('NYT with Divergence Penalty')


# Top 10 words
W_nyt_norm = normalize(W_nyt, norm='l1', axis=0)


for col in [0,5,10,17,22]:
    temp = np.argsort(W_nyt_norm[:,col])[::-1][0:10]
    print 'Column of W: ' + str(col)
    for j in temp:
        print nytworddict[j] + ' ' + str(W_nyt_norm[:,col][j])
    print '\n'


  