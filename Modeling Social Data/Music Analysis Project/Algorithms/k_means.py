from apk import apk
import numpy as np
from collections import defaultdict
from sklearn.cluster import KMeans

def rawkmeans(Mtrain, omegau, omegau_test, omegav, ncl=10):
    kmeans_setup = KMeans(n_clusters=ncl)
    kmeans_model = kmeans_setup.fit_transform(Mtrain)

    ulist = []
    slist = {}
    flatsonglist = {}
    notinOMEGAU = set()

    for i in xrange(0,ncl):
        cl = i
        sorted_array = np.argsort(kmeans_model.T[i])[0:10]
        sort = kmeans_model.T[i, sorted_array]
        for k in xrange(0,10):
            uindex = sorted_array[k]
            if cl in slist:
                if uindex in omegau:
                    slist[cl].append(omegau[uindex])
                else:
                    #print "This index is not in OMEGA_U Uindex=", uindex
                    notinOMEGAU.add(uindex)
            else:
                if uindex in omegau:
                    slist[cl] = [(omegau[uindex])]
                else:
                    #print "This index is not in OMEGA_U Uindex=", uindex 
                    notinOMEGAU.add(uindex)

    for cl in xrange(0,10):
        if cl in slist:
            flatsonglist[cl] = [item for sublist in slist[cl] for item in sublist]

    # assign one user to one cluster
    cl_user_dic = defaultdict(list)
    user_cl_dic = {}    

    #for i in xrange(0, len(kmeans_model)):
    #    cl_assignment = np.argmin(kmeans_model[i]) 
    #    cl_user_dic[cl_assignment].append(i)

    #for key, value in cl_user_dic.items():
    #    print key, len(value)

    for i in xrange(0, len(kmeans_model)):
        cl_assignment = np.argmin(kmeans_model[i]) 
        user_cl_dic[i] = cl_assignment

    # for each song how many users have played it
    cls_songs = {}

    for cl, sindexLIST in flatsonglist.items():
        nplaycnt = []
        for sindex in sindexLIST:
            tupole = (sindex, len(omegav[sindex]))
        nplaycnt.append(tupole) 
        sortsongs_t = sorted(nplaycnt, key=lambda x: x[1], reverse=True)
        sortsonsgs = [i[0] for i in sortsongs_t]
        cls_songs[cl] = sortsonsgs

    prediction = {}
    # list of users and the 500 songs
    for uindex in user_cl_dic:
        # which cluster is the user in
        cl = user_cl_dic[uindex]
        # what songs are in that cluser
        songlist = cls_songs[cl]
        prediction[uindex] = songlist
        
    apk_sum = 0
    rec = {}
    counter = 0
    for i in omegau_test:
        if i in omegau:
            rec[i] = [x for x in prediction[i] if x not in omegau[i]][0:500]
            apk_sum += apk(omegau_test[i], rec[i])
            counter += 1
            
    mapval = apk_sum/counter
    return mapval