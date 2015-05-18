from apk import apk
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

def NMF(Mtrain, omegau, omegau_test, iter=20, rank = 25):
    X = Mtrain.T

    rank = 25

    N1 = np.shape(Mtrain)[0]
    N2 = np.shape(Mtrain)[1]

    W = np.random.uniform(size=[N2,rank])
    H = np.random.uniform(size=[rank,N1])

    divobj = []
    for t in xrange(0,iter):
        temp1 = normalize(np.transpose(W), norm='l1', axis=1)
        purple = X / (np.dot(W,H) + 10**(-16))
        H = H * np.dot(temp1,purple)
        temp2 = normalize(np.transpose(H), norm='l1', axis=0) 
        purple = X / (np.dot(W,H) + 10**(-16))
        W = W * np.dot(purple,temp2)
        temp = np.sum((X * np.log(1/(np.dot(W,H) + 10**(-16)))) + (np.dot(W,H)))
        divobj.append(temp)
        
    plt.plot(divobj)
    plt.xlabel('Iteration')
    plt.ylabel('Objective function')
    plt.title('NMF with Divergence Penalty')
    
    rec_user = {}
    for user in  xrange(0,N1):
        song_ranks = np.dot(W, H[:,user])
        rec_user[user] = np.argsort(song_ranks)[::-1]

    apk_sum = 0
    rec = {}
    counter = 0
    for i in omegau_test:
        if i in omegau:
            rec[i] = [x for x in rec_user[i] if x not in omegau[i]][0:500]
            apk_sum += apk(omegau_test[i], rec[i])
            counter += 1
            
    mapval = apk_sum/counter
    return mapval