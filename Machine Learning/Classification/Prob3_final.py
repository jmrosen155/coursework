# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 12:35:25 2015

@author: Jordan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mode

xtrain = np.loadtxt('mnist_csv/Xtrain.txt', delimiter=",")
labeltrain = np.loadtxt('mnist_csv/label_train.txt', delimiter=",")
xtest = np.loadtxt('mnist_csv/Xtest.txt', delimiter=",")
labeltest = np.loadtxt('mnist_csv/label_test.txt', delimiter=",")
Q = np.loadtxt('mnist_csv/Q.txt', delimiter=",")

#Part 3a

#Calculates Euclidean distance between all testing and training points
distance = np.empty([500,5000])
for i in xrange(0,500):
    for j in xrange(0,5000):
        temp = 0
        for k in xrange(0,20):
            temp = temp + np.power((xtrain[j][k]-xtest[i][k]),2)
        distance[i][j] = np.power(temp,0.5)

#Get 5 closest indices and labels
ind = np.empty([500,5])
lab = np.empty([500,5])
for i in xrange(0,500):
    ind[i] = np.argsort(distance[i])[:5]
    lab[i] = labeltrain[ind[i].astype(int)]
    
labelk = np.empty([5,500])
#Note: k=0 corresponds to k=1 and so on...
for i in xrange(0,500):
    labelk[0][i] = lab[i][0]
    labelk[1][i] = mode(lab[i][0:2])[0]
    labelk[2][i] = mode(lab[i][0:3])[0]
    labelk[3][i] = mode(lab[i][0:4])[0]
    labelk[4][i] = mode(lab[i][0:5])[0]
    
#Confusion matrix
C1 = np.zeros([10,10])
C2 = np.zeros([10,10])
C3 = np.zeros([10,10])
C4 = np.zeros([10,10])
C5 = np.zeros([10,10])

for j in xrange(0,500):
    yp = labelk[0][j]
    yt = labeltest[j]
    C1[yt][yp] = C1[yt][yp] + 1
    
for j in xrange(0,500):
    yp = labelk[1][j]
    yt = labeltest[j]
    C2[yt][yp] = C2[yt][yp] + 1
    
for j in xrange(0,500):
    yp = labelk[2][j]
    yt = labeltest[j]
    C3[yt][yp] = C3[yt][yp] + 1
    
for j in xrange(0,500):
    yp = labelk[3][j]
    yt = labeltest[j]
    C4[yt][yp] = C4[yt][yp] + 1
    
for j in xrange(0,500):
    yp = labelk[4][j]
    yt = labeltest[j]
    C5[yt][yp] = C5[yt][yp] + 1

print 'Prediction Accuracy:'
print 'k=1:', np.trace(C1)/500
print 'k=2:', np.trace(C2)/500
print 'k=3:', np.trace(C3)/500
print 'k=4:', np.trace(C4)/500
print 'k=5:', np.trace(C5)/500

#Misclassified examples:

fig = plt.figure()

#k=1
#index: 10, 19, 140
print 'k=1:'
print 'True: ', labeltest[10], 'Predicted: ', labelk[0][10]
print 'True: ', labeltest[19], 'Predicted: ', labelk[0][19]
print 'True: ', labeltest[140], 'Predicted: ', labelk[0][140]
y1 = np.dot(Q, xtest[10])
plt.subplot(331)
plt.imshow(y1.reshape(28,28), cmap="Greys")
y2 = np.dot(Q,xtest[19])
plt.subplot(332)
plt.imshow(y2.reshape(28,28), cmap="Greys")
y3 = np.dot(Q,xtest[140])
plt.subplot(333)
plt.imshow(y3.reshape(28,28), cmap="Greys")

#k=3
#index: 10, 456, 492
print 'k=3:'
print 'True: ', labeltest[10], 'Predicted: ', labelk[2][10]
print 'True: ', labeltest[456], 'Predicted: ', labelk[2][456]
print 'True: ', labeltest[492], 'Predicted: ', labelk[2][492]
y1 = np.dot(Q, xtest[10])
plt.subplot(334)
plt.imshow(y1.reshape(28,28), cmap="Greys")
y2 = np.dot(Q,xtest[456])
plt.subplot(335)
plt.imshow(y2.reshape(28,28), cmap="Greys")
y3 = np.dot(Q,xtest[492])
plt.subplot(336)
plt.imshow(y3.reshape(28,28), cmap="Greys")

#k=5
#index: 10, 447, 455
print 'k=5:'
print 'True: ', labeltest[10], 'Predicted: ', labelk[4][10]
print 'True: ', labeltest[447], 'Predicted: ', labelk[4][447]
print 'True: ', labeltest[455], 'Predicted: ', labelk[4][455]
y1 = np.dot(Q, xtest[10])
plt.subplot(337)
plt.imshow(y1.reshape(28,28), cmap="Greys")
y2 = np.dot(Q,xtest[447])
plt.subplot(338)
plt.imshow(y2.reshape(28,28), cmap="Greys")
y3 = np.dot(Q,xtest[455])
plt.subplot(339)
plt.imshow(y3.reshape(28,28), cmap="Greys")


#Part 3b

j=0
xtr = np.empty([10,500,20])
for i in xrange(0,5000,500):
    xtr[j] = xtrain[i:i+500]
    j = j+1

mu = np.empty([10,20])
for i in xrange(0,10):
    mu[i] = np.sum(xtr[i], axis=0)/500
    
cov = np.empty([10,20,20])
for i in xrange(0,10):
    cov[i] = np.dot(np.transpose(xtr[i]-mu[i]), (xtr[i]-mu[i]))/500

BC  = np.empty([500,10])
for i in xrange(0,500): 
    for j in xrange(0,10):
        t1 = (1/np.power((2*np.pi),10))*0.1*(1/np.sqrt(np.linalg.det(cov[j])))
        t4 = (xtest[i]-mu[j])
        t3 = np.linalg.inv(cov[j])
        t2 = -0.5*np.transpose((xtest[i]-mu[j]))
        t5 = np.dot(t2,t3)
        t6 = np.dot(t5,t4)
        t7 = np.exp(t6)
        BC[i,j] = np.dot(t1,t7)

labelb = np.empty([500])
for i in xrange(0,500):
    labelb[i] = np.argmax(BC[i])

C6 = np.zeros([10,10])
for i in xrange(0,500):
    yp = labelb[i]
    yt = labeltest[i]
    C6[yt][yp] = C6[yt][yp] + 1

print 'Confusion Matrix:'
print(C6)    
print 'Prediction Accuracy:'
print 'Bayes classifier:', np.trace(C6)/500

#Mean of each Gaussian
fig = plt.figure()
for i in xrange(0,10):
    y = np.dot(Q, mu[i])
    plt.subplot(2,5,i+1)
    plt.imshow(y.reshape(28,28), cmap="Greys")
  
#Misclassified examples
#index: 10, 38, 480 
  
fig = plt.figure()

print 'Bayes classifier:'
print 'True: ', labeltest[10], 'Predicted: ', labelb[10]
print(BC[10])
print 'True: ', labeltest[38], 'Predicted: ', labelb[38]
print(BC[38])
print 'True: ', labeltest[480], 'Predicted: ', labelb[480]
print(BC[480])
y1 = np.dot(Q, xtest[10])
plt.subplot(131)
plt.imshow(y1.reshape(28,28), cmap="Greys")
y2 = np.dot(Q,xtest[38])
plt.subplot(132)
plt.imshow(y2.reshape(28,28), cmap="Greys")
y3 = np.dot(Q,xtest[480])
plt.subplot(133)
plt.imshow(y3.reshape(28,28), cmap="Greys")


#Part 3c

ones = np.zeros([5000,1]) + 1
xtrain1 = np.copy(xtrain)
xtrain1 = np.append(xtrain1,ones,axis=1)

j=0
xtr1 = np.empty([10,500,21])
for i in xrange(0,5000,500):
    xtr1[j] = xtrain1[i:i+500]
    j = j+1

w = np.zeros([10,21])
lik = np.zeros([10,1000])
for q in xrange(0,1000):
    grad = np.zeros([10,21])
    for i in xrange(0,10):
        for j in xrange(0,500):
            t1 = np.exp(np.dot(xtr1[i][j],w[i]))
            t1 = np.dot(xtr1[i][j],t1)
            t2 = np.dot(np.transpose(xtr1[i][j]),w[i])
            norm = 0        
            for k in xrange(0,10):
                norm = norm + np.exp(np.dot(xtr1[i][j],w[k]))
            grad[i] = grad[i] + (xtr1[i][j]-t1/norm)
            lik[i][q] = lik[i][q] + (t2-np.log(norm))
        w[i] = w[i] + 0.00002*grad[i]

#Convergence of likelihood for each class
'''
fig = plt.figure()
for i in xrange(0,10):
    plt.subplot(2,5,i)
    plt.plot(lik[i])
'''

likelihood_overall = np.sum(lik, axis=0)    
plt.plot(likelihood_overall)
plt.ylabel('log-likelihood')
plt.xlabel('iteration')

#Predicting labels for the test set 
ones = np.zeros([500,1]) + 1
xtest1 = np.copy(xtest)
xtest1 = np.append(xtest1,ones,axis=1)
  
liktest = np.zeros([500,10])  
for i in xrange(0,500):
    for j in xrange(0,10):
        t1 = np.exp(np.dot(xtest1[i],w[j]))
        t1 = np.dot(xtest1[i],t1)
        t2 = np.dot(np.transpose(xtest1[i]),w[j])
        norm = 0        
        for k in xrange(0,10):
            norm = norm + np.exp(np.dot(xtest1[i],w[k]))
        liktest[i][j] = (t2-np.log(norm))
    
labellog = np.empty([500])
for i in xrange(0,500):
    labellog[i] = np.argmax(liktest[i])

C7 = np.zeros([10,10])
for i in xrange(0,500):
    yp = labellog[i]
    yt = labeltest[i]
    C7[yt][yp] = C7[yt][yp] + 1

print 'Confusion Matrix:'
print(C7)    
print 'Prediction Accuracy:'
print 'Logistic regression:', np.trace(C7)/500    
    
    
#Misclassified examples
#index: 2, 477, 492 
  
fig = plt.figure()

print 'Logistic regression:'
print 'True: ', labeltest[2], 'Predicted: ', labellog[2]
print(liktest[2])
print 'True: ', labeltest[477], 'Predicted: ', labellog[477]
print(liktest[477])
print 'True: ', labeltest[492], 'Predicted: ', labellog[492]
print(liktest[492])
y1 = np.dot(Q, xtest[2])
plt.subplot(131)
plt.imshow(y1.reshape(28,28), cmap="Greys")
y2 = np.dot(Q,xtest[477])
plt.subplot(132)
plt.imshow(y2.reshape(28,28), cmap="Greys")
y3 = np.dot(Q,xtest[492])
plt.subplot(133)
plt.imshow(y3.reshape(28,28), cmap="Greys")      
