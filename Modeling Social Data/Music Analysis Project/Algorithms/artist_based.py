import numpy as np
import pandas as pd
import random
from collections import OrderedDict

from apk import apk

def artist_based(user_songs, artist_songdict, popularsonglist, omegau_test, omegau_train):
    apk_sum = 0

    for key_user_index in list(set(omegau_test).intersection(omegau_train)):
        songlist = []
        for key_artist_id in list(user_songs[user_songs.user_index==key_user_index].artist_id.values):
            songlist += artist_songdict[key_artist_id]
        # appending the popularsonglist to the generated songlist, assume 600 is more than enough to account for any overlaps
        songlist = list(OrderedDict.fromkeys(songlist + popularsonglist))[:600]
        # starting from np.delete, this function is just to remove the songs in songlist that already exist in omegau_train
        apk_sum += apk(omegau_test[key_user_index],np.delete(songlist,np.nonzero(np.in1d(songlist,omegau_train[key_user_index])))[:500])

    return apk_sum/len(list(set(omegau_test).intersection(omegau_train)))


