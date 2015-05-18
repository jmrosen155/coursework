import numpy as np
import pandas as pd
import random
from apk import apk

def MF(Mtrain, var, omega, omega_test, omegau, omegau_test, d, iter):
    
    N1 = np.shape(Mtrain)[0]
    N2 = np.shape(Mtrain)[1]

    users1 = {}
    songs1 = {}
    for i in range(N1):
        users1[i] = np.where(Mtrain[i] != 0)[0]

    for j in range(N2):
        songs1[j] = np.where(Mtrain[:,j] != 0)[0]

    I = np.identity(d)
    lamb = 10
    t1 = lamb*var*I

    mean = np.zeros([d])
    v = np.empty([d,N2])
    u = np.empty([N1,d])

    for j in xrange(0, N2):
        v[:,j] = np.random.multivariate_normal(mean,(1/float(lamb))*I)

    MAP=[]
    loglik=[]

    # Performing matrix factorization
    for c in xrange(0,iter):
        for i in range(N1):
            inner = np.dot(v[:,users1[i]], v[:,users1[i]].T)
            outer = np.dot(Mtrain[i][users1[i]], v[:,users1[i]].T)
            u[i] = np.dot((np.linalg.inv(t1 + inner)), outer.T).T

        for j in range(N2):
            inner = np.dot(u[songs1[j]].T, u[songs1[j]])
            outer = np.dot(Mtrain[songs1[j],j], u[songs1[j]])
            v[:,j] = np.dot(np.linalg.inv(t1 + inner), outer.T)

        sum4 = 0
        for (i, j) in omega:
            sum4 = sum4 + 0.5/var*np.power(Mtrain[i][j] - np.dot(u[i], v[:,j]),2)
        sum4 = -sum4
        sum5 = 0
        for i in xrange(0, N1):
            sum5 = sum5 + 0.5*lamb*np.sum(u[i]**2)
        sum5 = -sum5
        sum6 = 0
        for j in xrange(0, N2):
            sum6 = sum6 + 0.5*lamb*np.sum(v[:,j]**2)
        sum6 = -sum6
        loglik.append(sum4+sum5+sum6)

        # calculating every 5 iterations in order to save on computation time
        if c in ([0] + range(4,iter,5)):
            predict_m = np.dot(u,v)
    
            apk_sum = 0
            counter = 0

            rec = {}
            for i in list(set(omegau_test).intersection(omegau)):
                recommend = np.argsort(predict_m[i])[::-1]
                apk_sum += apk(omegau_test[i], np.delete(recommend,np.nonzero(np.in1d(recommend,omegau[i])))[:500])
                counter += 1

            MAP.append(apk_sum/counter)

    return MAP, loglik

# MF without calculating log likelihood to reduce compute time
def MF2(Mtrain, var, omegau, omegau_test, d, iter):
    
    N1 = np.shape(Mtrain)[0]
    N2 = np.shape(Mtrain)[1]

    users1 = {}
    songs1 = {}
    for i in range(N1):
        users1[i] = np.where(Mtrain[i] != 0)[0]

    for j in range(N2):
        songs1[j] = np.where(Mtrain[:,j] != 0)[0]

    I = np.identity(d)
    lamb = 10
    t1 = lamb*var*I

    mean = np.zeros([d])
    v = np.empty([d,N2])
    u = np.empty([N1,d])

    for j in xrange(0, N2):
        v[:,j] = np.random.multivariate_normal(mean,(1/float(lamb))*I)

    # Performing matrix factorization
    for c in xrange(0,iter):
        for i in range(N1):
            inner = np.dot(v[:,users1[i]], v[:,users1[i]].T)
            outer = np.dot(Mtrain[i][users1[i]], v[:,users1[i]].T)
            u[i] = np.dot((np.linalg.inv(t1 + inner)), outer.T).T

        for j in range(N2):
            inner = np.dot(u[songs1[j]].T, u[songs1[j]])
            outer = np.dot(Mtrain[songs1[j],j], u[songs1[j]])
            v[:,j] = np.dot(np.linalg.inv(t1 + inner), outer.T)

    predict_m = np.dot(u,v)
    
    apk_sum = 0
    counter = 0

    rec = {}
    for i in list(set(omegau_test).intersection(omegau)):
        recommend = np.argsort(predict_m[i])[::-1]
        apk_sum += apk(omegau_test[i], np.delete(recommend,np.nonzero(np.in1d(recommend,omegau[i])))[:500])
        counter += 1
    
    return apk_sum/counter

