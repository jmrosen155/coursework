# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:41:52 2015

@author: Jordan
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# Importing the data and separating into testing and training sets

x = np.loadtxt('cancer_csv/X.csv', delimiter=",")
xtest = x[0:183]
xtrain = x[183:684]
y = np.loadtxt('cancer_csv/y.csv', delimiter=",")
ytest = y[0:183]
ytrain = y[183:684]

# Part 1

def sample(n, w):
    cdf = np.cumsum(w)
    c = np.empty([n])
    for i in xrange(0,n):
        u = np.random.uniform()
        temp = np.where(u < cdf)
        c[i] = temp[0][0]
    return c
        

w = [0.1, 0.2, 0.3, 0.4]
w = np.asarray(w)  

fig = plt.figure()

for i in xrange(1,6):
    c = sample(i*100, w)
    plt.subplot(1,5,i)
    plt.hist(c)
    plt.xticks(xrange(0,4))
    s = 'n = ' + str(i*100)
    plt.xlabel(s)
    

# Part 2.1

n = len(xtrain)
weight = 1 / float(n)

iterations = 1000

epsilon = np.empty([iterations])
alpha = np.empty([iterations])
D = np.empty([iterations, n])
error_train = np.empty([iterations])
error_test = np.empty([iterations])

f_train = np.zeros([500])
f_test = np.zeros([183])

D[0] = np.ones([n])

D[0] = D[0] * weight

B = sample(n, D[0])

#t = 0
for t in xrange(0, iterations):

    xboot = np.empty([500,10])
    yboot = np.empty([500,1])
    row = 0
    pos = 0
    neg = 0
    for index in B:
        xboot[row] = xtrain[index]
        yboot[row] = ytrain[index]
        if yboot[row] == 1:
            pos = pos + 1
        else:
            neg = neg + 1
        row = row + 1
    
    pipos = float(pos)/len(yboot)
    pineg = float(neg)/len(yboot)
    
    xbootpos = np.empty([pos,10])
    xbootneg = np.empty([neg,10])
    
    pos = 0
    neg = 0
    for index in xrange(0, len(yboot)):
        if yboot[index] == 1:
            xbootpos[pos] = xboot[index]
            pos = pos + 1
        else:
            xbootneg[neg] = xboot[index]
            neg = neg + 1        
    
    mupos = np.empty([10])
    muneg = np.empty([10])
    mu = np.empty([10])
    mupos = np.sum(xbootpos, axis=0)/len(xbootpos)
    muneg = np.sum(xbootneg, axis=0)/len(xbootneg)
    mu = np.sum(xboot, axis=0)/len(xboot)
        
    #cov_temp = np.empty([10,10])
    #cov_temp = np.dot(np.transpose(xboot-mu), (xboot-mu))/len(xboot)
    
    #cov = np.empty([9,9])
    #for i in xrange(0,9):
        #for j in xrange(0,9):
            #cov[i][j] = cov_temp[i+1][j+1]
            
    
    xtemp = np.empty([500,9])
    for i in xrange(0,500):
        xtemp[i] = xboot[i][1:10]
        
    cov = np.empty([9,9])
    cov = np.dot(np.transpose(xtemp-mu[1:10]), (xtemp-mu[1:10]))/len(xtemp)
    
    
    
    t1 = math.log(pipos/pineg) 
    t2 = 0.5*np.dot(np.dot(np.transpose(mupos[1:10]+muneg[1:10]), np.linalg.inv(cov)), (mupos[1:10]-muneg[1:10]))
    wzero = t1 - t2
    w = np.dot(np.linalg.inv(cov), (mupos[1:10]-muneg[1:10]))
    waug = np.empty([10])
    waug[0] = wzero
    waug[1:10] = w
    
    BC_train = np.empty([500])
    ypred_train = np.empty([500])
    for i in xrange(0,500):
        BC_train[i] = np.dot(np.transpose(xtrain[i]), waug)
        if BC_train[i] > 0:
            ypred_train[i] = 1
        else:
            ypred_train[i] = -1
            
    
    
    
    
    BC_test = np.empty([183])
    ypred_test = np.empty([183])
    for i in xrange(0,183):
        BC_test[i] = np.dot(np.transpose(xtest[i]), waug)
        if BC_test[i] > 0:
            ypred_test[i] = 1
        else:
            ypred_test[i] = -1
    
    
    
    epsilon[t] = 0
    for i in xrange(0,500):
        if ytrain[i] != ypred_train[i]:
            epsilon[t] = epsilon[t] + D[t][i]
            
    alpha[t] = 0.5 * math.log((1-epsilon[t])/epsilon[t])
    
    
    f_pred_train = np.empty([500])
    for i in xrange(0, 500):
        temp = alpha[t] * ypred_train[i]
        f_train[i] = f_train[i] + temp
        if f_train[i] > 0:
            f_pred_train[i] = 1
        else:
            f_pred_train[i] = -1
            
    C = np.zeros([2,2])
    for i in xrange(0,500):
        if f_pred_train[i] == 1:
            yp = 0
        else:
            yp = 1
        if ytrain[i] == 1:
            yt = 0
        else:
            yt = 1
        C[yt][yp] = C[yt][yp] + 1
        
    error_train[t] = 1 - (np.trace(C)/500)
            
    f_pred_test = np.empty([183])
    for i in xrange(0, 183):
        temp = alpha[t] * ypred_test[i]
        f_test[i] = f_test[i] + temp
        if f_test[i] > 0:
            f_pred_test[i] = 1
        else:
            f_pred_test[i] = -1
            
    C = np.zeros([2,2])
    for i in xrange(0,183):
        if f_pred_test[i] == 1:
            yp = 0
        else:
            yp = 1
        if ytest[i] == 1:
            yt = 0
        else:
            yt = 1
        C[yt][yp] = C[yt][yp] + 1
    
    
    error_test[t] = 1 - (np.trace(C)/183)
    
    if t != iterations-1:
        for i in xrange(0,500):
            D[t+1][i] = D[t][i] * math.exp(-alpha[t]*ytrain[i]*ypred_train[i])
            
        D[t+1] = D[t+1] / sum(D[t+1])
        
        B = sample(n, D[t+1])
  

# Part 2.2

plt.plot(error_train)  
plt.plot(error_test)
plt.ylabel('Prediction Error')
plt.xlabel('Iteration')
plt.legend(['Training Error', 'Testing Error'], loc='upper right')
plt.show()

# Part 2.3

pos = 0
neg = 0
for i in xrange(0,500):
    if ytrain[i] == 1:
        pos = pos + 1
    else:
        neg = neg + 1
    row = row + 1

pipos = float(pos)/len(ytrain)
pineg = float(neg)/len(ytrain)

xtrainpos = np.empty([pos,10])
xtrainneg = np.empty([neg,10])

pos = 0
neg = 0
for index in xrange(0, len(ytrain)):
    if ytrain[index] == 1:
        xtrainpos[pos] = xtrain[index]
        pos = pos + 1
    else:
        xtrainneg[neg] = xtrain[index]
        neg = neg + 1        

mupos = np.empty([10])
muneg = np.empty([10])
mu = np.empty([10])
mupos = np.sum(xtrainpos, axis=0)/len(xtrainpos)
muneg = np.sum(xtrainneg, axis=0)/len(xtrainneg)
mu = np.sum(xtrain, axis=0)/len(xtrain)
        

xtemp = np.empty([500,9])
for i in xrange(0,500):
    xtemp[i] = xtrain[i][1:10]
    
cov = np.empty([9,9])
cov = np.dot(np.transpose(xtemp-mu[1:10]), (xtemp-mu[1:10]))/len(xtemp)


t1 = math.log(pipos/pineg) 
t2 = 0.5*np.dot(np.dot(np.transpose(mupos[1:10]+muneg[1:10]), np.linalg.inv(cov)), (mupos[1:10]-muneg[1:10]))
wzero = t1 - t2
w = np.dot(np.linalg.inv(cov), (mupos[1:10]-muneg[1:10]))
waug = np.empty([10])
waug[0] = wzero
waug[1:10] = w

'''
BC_train = np.empty([500])
ypred_train = np.empty([500])
for i in xrange(0,500):
    BC_train[i] = np.dot(np.transpose(xtrain[i]), waug)
    if BC_train[i] > 0:
        ypred_train[i] = 1
    else:
        ypred_train[i] = -1
'''        

#BC = np.empty([183])
ypred = np.empty([183])
for i in xrange(0,183):
    BC = np.dot(np.transpose(xtest[i]), waug)
    if BC > 0:
        ypred[i] = 1
    else:
        ypred[i] = -1
        
        
C = np.zeros([2,2])
for i in xrange(0,183):
    if ypred[i] == 1:
        yp = 0
    else:
        yp = 1
    if ytest[i] == 1:
        yt = 0
    else:
        yt = 1
    C[yt][yp] = C[yt][yp] + 1


error_test_noboost = 1 - (np.trace(C)/183)
print 'Testing accuracy without boosting: ', 1 - error_test_noboost


# Part 2.4

plt.subplot(1,2,1)
plt.plot(alpha)  
plt.ylabel('alpha')
plt.xlabel('Iteration')


plt.subplot(1,2,2)
plt.plot(epsilon)  
plt.ylabel('epsilon')
plt.xlabel('Iteration')
plt.show()

# Part 2.5

datapoint1 = np.empty([1000])
datapoint2 = np.empty([1000])
datapoint3 = np.empty([1000])

for i in xrange(0,1000):
    datapoint1[i] = D[i][0]
    datapoint2[i] = D[i][7]
    datapoint3[i] = D[i][494]

plt.subplot(1,3,1)    
plt.plot(datapoint1)
plt.ylabel('Weight')
plt.subplot(1,3,2)  
plt.plot(datapoint2)
plt.xlabel('Iteration')
plt.subplot(1,3,3)
plt.plot(datapoint3)
plt.show()








# Part 3.1

n = len(xtrain)
weight = 1 / float(n)

iterations = 1000

step = 0.1

epsilon = np.empty([iterations])
alpha = np.empty([iterations])
D = np.empty([iterations, n])
error_train = np.empty([iterations])
error_test = np.empty([iterations])

f_train = np.zeros([500])
f_test = np.zeros([183])

D[0] = np.ones([n])

D[0] = D[0] * weight

B = sample(n, D[0])

#t = 0
for t in xrange(0, iterations):

    xboot = np.empty([500,10])
    yboot = np.empty([500,1])
    row = 0

    for index in B:
        xboot[row] = xtrain[index]
        yboot[row] = ytrain[index]
        row = row + 1
        
    
    xyboot = np.empty([500,11])
    for i in xrange(0, 500):
        xyboot[i][0] = yboot[i]
        xyboot[i][1:11] = xboot[i]
        
    np.random.shuffle(xyboot) 
    for i in xrange(0, 500):
        yboot[i] = xyboot[i][0] 
        xboot[i] = xyboot[i][1:11] 
    
    
    
    waug = np.zeros([10])
    
    for i in xrange(0, n):
        sigmoid = 1 / (1 + np.exp(-yboot[i]*np.dot(np.transpose(xboot[i]), waug)))
        waug = waug + step * (1-sigmoid)*yboot[i]*xboot[i]
    
    
    Log_train = np.empty([500])
    ypred_train = np.empty([500])
    for i in xrange(0,500):
        Log_train[i] = np.dot(np.transpose(xtrain[i]), waug)
        if Log_train[i] > 0:
            ypred_train[i] = 1
        else:
            ypred_train[i] = -1
            
    
    
    
    
    Log_test = np.empty([183])
    ypred_test = np.empty([183])
    for i in xrange(0,183):
        Log_test[i] = np.dot(np.transpose(xtest[i]), waug)
        if Log_test[i] > 0:
            ypred_test[i] = 1
        else:
            ypred_test[i] = -1
    
    
    
    epsilon[t] = 0
    for i in xrange(0,500):
        if ytrain[i] != ypred_train[i]:
            epsilon[t] = epsilon[t] + D[t][i]
            
    alpha[t] = 0.5 * math.log((1-epsilon[t])/epsilon[t])
    
    
    f_pred_train = np.empty([500])
    for i in xrange(0, 500):
        temp = alpha[t] * ypred_train[i]
        f_train[i] = f_train[i] + temp
        if f_train[i] > 0:
            f_pred_train[i] = 1
        else:
            f_pred_train[i] = -1
            
    C = np.zeros([2,2])
    for i in xrange(0,500):
        if f_pred_train[i] == 1:
            yp = 0
        else:
            yp = 1
        if ytrain[i] == 1:
            yt = 0
        else:
            yt = 1
        C[yt][yp] = C[yt][yp] + 1
        
    error_train[t] = 1 - (np.trace(C)/500)
            
    f_pred_test = np.empty([183])
    for i in xrange(0, 183):
        temp = alpha[t] * ypred_test[i]
        f_test[i] = f_test[i] + temp
        if f_test[i] > 0:
            f_pred_test[i] = 1
        else:
            f_pred_test[i] = -1
            
    C = np.zeros([2,2])
    for i in xrange(0,183):
        if f_pred_test[i] == 1:
            yp = 0
        else:
            yp = 1
        if ytest[i] == 1:
            yt = 0
        else:
            yt = 1
        C[yt][yp] = C[yt][yp] + 1
    
    
    error_test[t] = 1 - (np.trace(C)/183)
    
    if t != iterations-1:
        for i in xrange(0,500):
            D[t+1][i] = D[t][i] * math.exp(-alpha[t]*ytrain[i]*ypred_train[i])
            
        D[t+1] = D[t+1] / sum(D[t+1])
        
        B = sample(n, D[t+1])
  

# Part 3.2

plt.plot(error_train)  
plt.plot(error_test)
plt.ylabel('Prediction Error')
plt.xlabel('Iteration')
plt.legend(['Training Error', 'Testing Error'], loc='upper right')
plt.show()

# Part 3.3

waug = np.zeros([10])
    
for i in xrange(0, 1000):
    t1 = np.zeros([10])
    for j in xrange(0, n):
        sigmoid = 1 / (1 + np.exp(-ytrain[j]*np.dot(np.transpose(xtrain[j]), waug)))
        t1 = t1 + (1 - sigmoid)*ytrain[j]*xtrain[j]
    waug = waug + step * t1


     

#Logistic = np.empty([183])
ypred = np.empty([183])
for i in xrange(0,183):
    Logistic = np.dot(np.transpose(xtest[i]), waug)
    if Logistic > 0:
        ypred[i] = 1
    else:
        ypred[i] = -1
        
        
C = np.zeros([2,2])
for i in xrange(0,183):
    if ypred[i] == 1:
        yp = 0
    else:
        yp = 1
    if ytest[i] == 1:
        yt = 0
    else:
        yt = 1
    C[yt][yp] = C[yt][yp] + 1


error_test_noboost = 1 - (np.trace(C)/183)
print 'Testing accuracy without boosting: ', 1 - error_test_noboost


# Part 3.4

plt.subplot(1,2,1)
plt.plot(alpha)  
plt.ylabel('alpha')
plt.xlabel('Iteration')


plt.subplot(1,2,2)
plt.plot(epsilon)  
plt.ylabel('epsilon')
plt.xlabel('Iteration')
plt.show()

# Part 3.5

datapoint1 = np.empty([1000])
datapoint2 = np.empty([1000])
datapoint3 = np.empty([1000])

for i in xrange(0,1000):
    datapoint1[i] = D[i][0]
    datapoint2[i] = D[i][7]
    datapoint3[i] = D[i][75]

plt.subplot(1,3,1)    
plt.plot(datapoint1)
plt.ylabel('Weight')
plt.subplot(1,3,2)  
plt.plot(datapoint2)
plt.xlabel('Iteration')
plt.subplot(1,3,3)
plt.plot(datapoint3)
plt.show()

