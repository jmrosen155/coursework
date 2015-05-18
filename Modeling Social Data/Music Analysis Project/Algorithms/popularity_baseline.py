import numpy as np
import pandas as pd

from apk import apk

def popularity_baseline(trainsub,omegau_train,omegau_test):
    # generating the list of songs ordered by number of counts and number of plays
    groupcount = trainsub[trainsub.plays>0].groupby('song_index').count().sort('plays', ascending=False).reset_index()
    topcounts = groupcount.song_index.values
    groupsum = trainsub[trainsub.plays>0].groupby('song_index').sum().sort('plays', ascending=False).reset_index()
    topplays = groupsum.song_index.values

    num = len(list(set(omegau_test).intersection(omegau_train)))

    # calculating map for songs by number of counts
    apk_sum_count = 0
    for i in list(set(omegau_test).intersection(omegau_train)):
        apk_sum_count += apk(omegau_test[i],np.delete(topcounts,np.nonzero(np.in1d(topcounts,omegau_train[i])))[:500])

    # calculating map for songs by number of plays
    apk_sum_plays = 0
    for i in list(set(omegau_test).intersection(omegau_train)):
        apk_sum_plays += apk(omegau_test[i],np.delete(topplays,np.nonzero(np.in1d(topplays,omegau_train[i])))[:500])

    return apk_sum_count/num, apk_sum_plays/num


